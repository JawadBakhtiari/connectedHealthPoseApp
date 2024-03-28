'''Class for storing and retreiving video data.
Notes:
    - Before a clip has finished, video data is stored locally as images within a directory
    - When a clip finishes, these images are converted into a video and stored in cloud storage
    - The local image directoy is deleted once it has been converted to a video and store in cloud storage
'''

import os
import cv2
import shutil
import tempfile
import numpy as np
import data.datastore.const as const
from PIL import Image
from data.datastore.cloud import get_blob_client
import base64
import io


class VideoStore:
    def __init__(self, sid: str, clip_num: str):
        '''
        Args:
            sid (str)       - the id of the session
            clip_num (str)  - the clip number within this session
        '''
        self.sid = sid
        self.clip_num = clip_num
        self.images = None
        self.video_path = None

    def get_video_path(self):
        '''Return the path to the video file for this clip.'''
        return os.path.join(tempfile.gettempdir(), self.get_video_name())

    def get_images_path(self):
        '''Return the path to the directory containing images for this clip.'''
        path = os.path.dirname(__file__)
        return os.path.join(path, "sessions", "images", self.get_images_name())

    def set(self, images: list):
        if not isinstance(images, list):
            raise TypeError('images must be of type list')
        self.images = images

    def get_images_name(self):
        '''Return the name that should be used to identify the directory containing images for this clip.
        '''
        return f"images_{self.sid}_{self.clip_num}"

    def get_video_name(self):
        '''Return the name that should be used to identify the video for a clip.
        '''
        return f"vid_{self.sid}_{self.clip_num}.mp4"

    def populate_video(self):
        '''Load video from cloud storage into a video file, store path to this file
        in self.video_path. Return True on success, False if video does not exist
        in cloud storage.     
        '''
        blob_client = get_blob_client(
            const.AZ_CLIPS_CONTAINER_NAME, self.get_video_name())
        if blob_client.exists():
            self.video_path = os.path.join(
                tempfile.gettempdir(), self.get_video_name())
            with open(self.video_path, "wb") as f:
                video_data = blob_client.download_blob()
                video_data.readinto(f)
            return True
        else:
            return False

    def _get_next_image_number(self, directory):
        '''Get the next image number to be used in the given directory, such that images
        all have unique image numbers.
        '''
        existing_files = os.listdir(directory)
        if existing_files:
            highest_num = max(int(f.split("img")[-1].split(".jpg")[0])
                              for f in existing_files if f.startswith("img") and f.endswith(".jpg"))
            return highest_num + 1
        else:
            return 0

    def write_images_locally(self):
        '''Write the image data to local storage on the file system.
        '''
        directory = self.get_images_path()
        os.makedirs(directory, exist_ok=True)

        start = self._get_next_image_number(directory)

        # JPG
        for i in range(len(self.images)):
            image = Image.open(io.BytesIO(
                base64.decodebytes(bytes(self.images[i], "utf-8"))))
            image.save(os.path.join(directory, f"img{start+i}.jpg"))

        # # RGB
        # for i, image_array in enumerate(self.images, start=start):
        #     image = Image.fromarray(np.array(image_array, dtype='uint8'))
        #     image.save(os.path.join(directory, f"img{i}.jpg"))

    def write_video_to_cloud(self, fps=15):
        '''Convert directory of images for this clip into a video and write this video to
        cloud storage. Delete local copies of video/images for this clip.'''
        images_path = self.get_images_path()

        # ensure that images are sorted correctly
        images = sorted([img for img in os.listdir(images_path) if img.endswith(
            '.jpg')], key=lambda x: int(x[3:len(x)-4]))

        # Get the first image to get dimensions
        image_path = os.path.join(images_path, images[0])
        frame = cv2.imread(image_path)
        height, width, _ = frame.shape

        # Create video from images
        video_name = self.get_video_name()
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter(video_name, fourcc, fps, (width, height))
        for image in images:
            image_path = os.path.join(images_path, image)
            frame = cv2.imread(image_path)
            video.write(frame)
        video.release()

        # Upload the video to cloud
        blob_client = get_blob_client(
            const.AZ_CLIPS_CONTAINER_NAME, video_name)
        with open(video_name, "rb") as f:
            blob_client.upload_blob(f, overwrite=True)

        # Remove local copy of video and images directory from local storage
        os.remove(video_name)
        shutil.rmtree(images_path)

    def delete(self):
        '''Delete the video file for a given clip from cloud storage.'''
        blob_client = get_blob_client(
            const.AZ_CLIPS_CONTAINER_NAME, self.get_video_name())

        if blob_client.exists():
            blob_client.delete_blob()
