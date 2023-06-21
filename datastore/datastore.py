import os
import orjson
import json
import datastore.const as const
from azure.storage.blob import BlobServiceClient

class DataStore:
    def __init__(self):
        self.clip = {}

    def get(self):
        return self.clip

    def set(self, store):
        if not isinstance(store, dict):
            raise TypeError('store must be of type dictionary')
        self.clip = store
    
    def populate_local(self, sid, clip_num):
        ''' KEEP VERSION FOR LOCAL STORAGE UNTIL BLOB STORAGE FINALISED
        Populate clip dict with the contents of a specific clip file from local storage.
        Return true if clip file already existed, false otherwise.

        Args:   sid         (str)  - the uuid of the session being searched 
                clip_num    (int)  - the clip number of this clip           
        '''
        path = os.path.dirname(__file__)
        try:
            with open(path + "/sessions/" + self.get_name(sid, clip_num) + ".json", "r") as f:
                self.clip = orjson.loads(f.read())
            return True
        except FileNotFoundError:
            return False
        
    def populate(self, sid, clip_num):
        '''Populate clip dict with the contents of a specific clip from a session from cloud storage.
        Return true if clip file already exists, false otherwise.

        Args:   sid         (str)  - the uuid of the session being searched 
                clip_num    (int)  - the clip number of this clip       
        '''
        # Create a blob client using the local file name as the name for the blob
        blob_service_client = BlobServiceClient.from_connection_string(const.AZ_CON_STR)
        blob_client = blob_service_client.get_blob_client(const.AZ_CONTAINER_NAME, self.get_name(sid, clip_num))

        if blob_client.exists():
            # Download the blob from that clip as a string and convert to json
            clip_data_string = blob_client.download_blob().content_as_text()
            self.clip = json.loads(clip_data_string)
            return True
        else:
            # No blob exists, for the moment return false to signify this
            return False

    def write_clip_locally(self, sid, clip_num):
        '''Write a clip to local storage on the file system. If there is already data stored

        Args:
            sid (str) - the UUID of the session being written
        '''
        path = os.path.dirname(__file__)
        filename = self.get_name(sid, clip_num)
        file_path = os.path.join(path, "sessions", filename)

        # Check if the file already exists
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                existing_data = json.load(f)  # Load existing data from the file
        else:
            existing_data = {}  # Create a new dictionary if the file doesn't exist

        # Update the existing data with the new frame data
        existing_data.update(self.clip)

        with open(file_path, "w") as f:
            json.dump(existing_data, f, indent=4)

    def write_session_to_cloud(self, sid):
        '''Write all clips that are stored locally for a session to Azure Blob storage. Remove
        all local copies of clips from sessions.

        Args:
            sid (str) - the UUID of the session being written
        '''
        session_data = {}
        # Iterate through the local files in the sessions directory
        path = os.path.dirname(__file__)
        directory = os.path.join(path, "sessions")
        for filename in os.listdir(directory):
            if filename.startswith(f"session_{sid}_"):
                file_path = os.path.join(directory, filename)
                with open(file_path, "r") as f:
                    clip_num = int(filename.split("_")[-1].split(".")[0])
                    session_data[clip_num] = json.load(f)

                # Delete the local file
                os.remove(file_path)

        # Upload the session data to Azure Blob Storage
        if session_data:
            # Create a blob service client
            blob_service_client = BlobServiceClient.from_connection_string(const.AZ_CON_STR)

            # Iterate through the session data and upload/update blobs
            for clip_num, frames in session_data.items():
                filename = self.get_name(sid, clip_num)
                blob_client = blob_service_client.get_blob_client(const.AZ_CONTAINER_NAME, filename)

                if blob_client.exists():
                    # Shouldn't be reached, but handle this case just to be safe
                    downloaded_bytes = blob_client.download_blob().readall()
                    existing_data = json.loads(downloaded_bytes)
                    # Append the new frame to the existing clip data
                    existing_data.update(frames)
                    updated_clip_data_bytes = json.dumps(existing_data).encode('utf-8')

                    # Upload the updated clip data (overwrite with updated information)
                    blob_client.upload_blob(updated_clip_data_bytes, overwrite=True)
                else:
                    # Upload the clip data as a new blob
                    clip_data_bytes = json.dumps(frames).encode('utf-8')
                    blob_client.upload_blob(clip_data_bytes)


    def get_name(self, sid, clip_num):
        '''Return the name that should be used to identify this clip.

        Args:   sid         (str)  - the uuid of the session being searched 
                clip_num    (int)  - the clip number of this clip   
        '''
        return f"session_{sid}_{clip_num}"
