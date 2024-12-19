import os
import tempfile
import data.datastore.const as const
from data.datastore.cloud import get_blob_client

class VideoStore:
    '''
    Handle the storage and retrieval of video data for a clip.
    '''
    def __init__(self, sid: str, clip_num: str) -> None:
        '''
        Args:
            sid (str)       - the id of the session
            clip_num (str)  - the clip number within this session
        '''
        self.sid = sid
        self.clip_num = clip_num


    def get(self) -> str:
        '''
        Load the video data for this clip into a file and return the path to this file.

        Raises:
            ValueError: if video data for this clip is not found.
        '''
        blob_client = get_blob_client(const.AZ_VIDEOS_CONTAINER_NAME, self.get_name())
        if blob_client.exists():
            video_path = os.path.join(tempfile.gettempdir(), self.get_name())
            with open(video_path, "wb") as f:
                blob_client.download_blob().readinto(f)
            return video_path
        raise ValueError(
            f"video from clip with sid '{self.sid}' and clip number '{self.clip_num}' not found"
        )
    

    def write(self, video: bytes) -> None:
        '''
        Store the video data for this clip.
        If there is already some video data, it is overwritten.
        '''
        blob_client = get_blob_client(const.AZ_VIDEOS_CONTAINER_NAME, self.get_name())
        blob_client.upload_blob(video, overwrite=True)


    def delete(self) -> None:
        '''
        Delete the video file for a this clip from cloud storage.
        '''
        blob_client = get_blob_client(const.AZ_VIDEOS_CONTAINER_NAME, self.get_name())
        if blob_client.exists():
            blob_client.delete_blob()


    def get_name(self) -> str:
        '''
        Return the name that should be used to identify the video for this clip.
        '''
        return f"{self.sid}_{self.clip_num}.MOV"
