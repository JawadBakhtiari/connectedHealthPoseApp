'''Class for storing and retreiving pose data (keypoints) '''

import os
import json
import data.datastore.const as const
from data.datastore.cloud import get_blob_client

class PoseStore:
    def __init__(self, sid: str, clip_num: str):
        '''
        Args:
            sid (str)       - the id of the session
            clip_num (str)  - the clip number within this session
        '''
        self.sid = sid
        self.clip_num = clip_num
        self.poses = []


    def get(self):
        return self.poses


    def set(self, poses: list):
        if not isinstance(poses, list):
            raise TypeError('poses must be of type list')
        # restructure formatting of pose data so it's easier to interact with
        self.poses = list(map(lambda p: p[0], poses))


    def get_name(self):
        '''Return the name that should be used to identify the file containing poses for this clip.
        '''
        return f"poses_{self.sid}_{self.clip_num}"
    

    def get_path(self):
        '''Return the path to the file containing pose data for this clip in local storage.'''
        path = os.path.dirname(__file__)
        filename = PoseStore.get_name(self.sid, self.clip_num) + ".json"
        return os.path.join(path, "sessions", "poses", filename)


    def populate(self):
        '''Populate clip dict with the contents of a specific clip from a session from cloud storage.
        Return true if clip file already exists, false otherwise.'''
        blob_client = get_blob_client(const.AZ_POSES_CONTAINER_NAME, self.get_name())

        if blob_client.exists():
            # Download the blob from that clip as a string and convert to json
            pose_data_string = blob_client.download_blob().content_as_text()
            self.poses = json.loads(pose_data_string)
            return True
        else:
            return False


    def write_locally(self):
        '''Write poses to file stored on file system.'''
        file_path = self.get_path()

        # Check if the file already exists
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                existing_data = json.load(f)  # Load existing data from the file
        else:
            existing_data = []  # Create a new dictionary if the file doesn't exist

        # Update the existing data with the new pose data
        existing_data += self.poses
        with open(file_path, "w") as f:
            json.dump(existing_data, f, indent=4)


    def write_to_cloud(self):
        '''Write pose data for a given clip to cloud storage, delete local copy of pose data.'''
        file_path = self.get_path()

        try: 
            with open(file_path, "r") as f:
                pose_data = json.load(f)
                blob_client = get_blob_client(const.AZ_POSES_CONTAINER_NAME, self.get_name())
                if blob_client.exists():
                    # Shouldn't be reached, but handle this case just to be safe
                    downloaded_bytes = blob_client.download_blob().readall()
                    existing_data = json.loads(downloaded_bytes)
                    existing_data.update(pose_data)
                    updated_clip_data_bytes = json.dumps(existing_data).encode('utf-8')

                    # Upload the updated clip data (overwrite with updated information)
                    blob_client.upload_blob(updated_clip_data_bytes, overwrite=True)
                else:
                    # Upload the clip data as a new blob
                    pose_data_bytes = json.dumps(pose_data).encode('utf-8')
                    blob_client.upload_blob(pose_data_bytes)
        except:
            print(f"Failed to upload clip sid: {self.sid} clip_num: {self.clip_num} to cloud storage.")


    def delete(self):
        '''Delete the pose data for a given clip from cloud storage.'''
        blob_client = get_blob_client(const.AZ_POSES_CONTAINER_NAME, self.get_name())

        if blob_client.exists():
            blob_client.delete_blob()
