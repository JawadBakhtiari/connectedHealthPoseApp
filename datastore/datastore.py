import os
import orjson
import json
import datastore.const as const
from azure.storage.blob import BlobServiceClient

class Sessionstore:
    def __init__(self):
        self.session = {}
        self.local_buffer = {}  # Local buffer for frames
    
    def print_buffer(self):
        print(self.local_buffer)

    def get(self):
        return self.session

    def set(self, store):
        if not isinstance(store, dict):
            raise TypeError('store must be of type dictionary')
        self.session = store
    
    def populate_local(self, sid):
        ''' KEEP VERSION FOR LOCAL STORAGE UNTIL BLOB STORAGE FINALISED
        Populate session dict with the contents of a specific session file.
        Return true if session file already existed, false otherwise.

        Args:   sid (str)  - the uuid of the session being searched         
        '''
        path = os.path.dirname(__file__)
        try:
            with open(path + "/sessions/session_" + str(sid) + ".json", "r") as f:
                self.session = orjson.loads(f.read())
            return True
        except FileNotFoundError:
            return False
        
    def populate(self, sid):
        '''Populate session dict with the contents of a specific session file from
        Azure blob storage.
        Return true if session file already exists, false otherwise.

        Args:   sid (str)  - the uuid of the session being searched         
        '''

        print(f'Before get_name, sid is: {sid}')

        # Create a blob client using the local file name as the name for the blob
        blob_service_client = BlobServiceClient.from_connection_string(const.AZ_CON_STR)
        blob_client = blob_service_client.get_blob_client(const.AZ_CONTAINER_NAME, self.get_name(sid))

        if blob_client.exists():
            # Download the blob from that session as a string and convert to json
            session_data_string = blob_client.download_blob().content_as_text()
            self.session = json.loads(session_data_string)
            return True
        else:
            # No blob exists, for the moment return false to signify this
            return False

    def write_local(self, sid, clipNum):
        ''' KEEP VERSION FOR LOCAL STORAGE UNTIL BLOB STORAGE FINALISED'''
        # path = os.path.dirname(__file__)
        # with open(path + "/sessions/session_" + str(sid) + "_" + str(clipNum) + ".json", "w") as f:
        #     json.dump(self.session, f, indent=4)

        ## NEW: includes appending frames to a session_clipnum
        path = os.path.dirname(__file__)
        filename = f"session_{sid}_{clipNum}.json"
        file_path = os.path.join(path, "sessions", filename)

        # Check if the file already exists
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                existing_data = json.load(f)  # Load existing data from the file
        else:
            existing_data = {}  # Create a new dictionary if the file doesn't exist

        # Update the existing data with the new frame data
        existing_data.update(self.session)

        with open(file_path, "w") as f:
            json.dump(existing_data, f, indent=4)


    def buffer_frames(self, sid, clipNum, frame_data):
        '''Buffer the frame data locally.

        Args:
            sid (str) - the uuid of the session
            clipNum (int) - the clip number in the session
            frame_data (dict) - the frame data
        '''
        # Use sid and clipNum as the key
        key = f"{sid}_{clipNum}"

        # If the key exists, merge the new frame data with the existing data,
        # else create a new dictionary with the frame data
        if key in self.local_buffer:
            for frame_number, keypoints in frame_data.items():
                if frame_number in self.local_buffer[key]:
                    self.local_buffer[key][frame_number].extend(keypoints)
                else:
                    self.local_buffer[key][frame_number] = keypoints
        else:
            self.local_buffer[key] = frame_data


    # def write(self, sid, sessionFinished=False):
    #     '''If Azure blob exists for this session, append current session data to this blob.
    #     Otherwise, create a new blob for this session and store session data in new blob.

    #     Args:   
    #         sid (str)  - the uuid of the session being written  
    #         sessionFinished (bool) - whether the session has been completed
    #     '''
    #     # Write to cloud storage only when the session has been completed
    #     if sessionFinished:
    #         # Concatenate all buffered frames in order
    #         for clipNum in sorted(self.local_buffer.keys()):
    #             self.session_frames = self.local_buffer[clipNum]
                
    #             # Create a blob client 
    #             blob_service_client = BlobServiceClient.from_connection_string(const.AZ_CON_STR)
    #             blob_client = blob_service_client.get_blob_client(const.AZ_CONTAINER_NAME, self.get_name(clipNum))

    #             # Upload the session data.
    #             # if blob under that sessionId exists, append frames
    #             if blob_client.exists():
    #                 # Download the existing session data 
    #                 downloaded_bytes = blob_client.download_blob().readall()
    #                 existing_data = json.loads(downloaded_bytes)

    #                 # Append the new frame to the existing session data
    #                 existing_data.extend(self.session_frames)
    #                 updated_session_data_bytes = json.dumps(existing_data).encode('utf-8')

    #                 # Upload the updated session data (overwrite with updated information)
    #                 blob_client.upload_blob(updated_session_data_bytes)
    #             else:
    #                 # If the sessionId does not exist, upload the session data as a new blob
    #                 session_data_bytes = json.dumps(self.session_frames).encode('utf-8')
    #                 blob_client.upload_blob(session_data_bytes)

    #         # Clear the local buffer
    #         self.local_buffer = {}

    

    def write(self, sid, sessionFinished=False):
        '''If Azure blob exists for this session, append current session data to this blob.
        Otherwise, create a new blob for this session and store session data in a new blob.

        Args:
            sid (str) - the UUID of the session being written
            sessionFinished (bool) - whether the session has been completed
        '''
        if sessionFinished:
            # Create a dictionary to hold the session data
            session_data = {}

            # Iterate through the local files in the sessions directory
            path = os.path.dirname(__file__)
            directory = os.path.join(path, "sessions")
            for filename in os.listdir(directory):
                if filename.startswith(f"session_{sid}_"):
                    file_path = os.path.join(directory, filename)
                    with open(file_path, "r") as f:
                        clipNum = int(filename.split("_")[-1].split(".")[0])
                        session_data[clipNum] = json.load(f)

                    # Delete the local file
                    os.remove(file_path)

            # Upload the session data to Azure Blob Storage
            if session_data:
                # Create a blob service client
                blob_service_client = BlobServiceClient.from_connection_string(const.AZ_CON_STR)

                # Iterate through the session data and upload/update blobs
                for clipNum, frames in session_data.items():
                    filename = f"session{sid}_{clipNum}"
                    blob_client = blob_service_client.get_blob_client(const.AZ_CONTAINER_NAME, filename)

                    if blob_client.exists():
                        # Download the existing session data
                        downloaded_bytes = blob_client.download_blob().readall()
                        existing_data = json.loads(downloaded_bytes)

                        # Append the new frame to the existing session data
                        existing_data.extend(frames)
                        updated_session_data_bytes = json.dumps(existing_data).encode('utf-8')

                        # Upload the updated session data (overwrite with updated information)
                        blob_client.upload_blob(updated_session_data_bytes)
                    else:
                        # Upload the session data as a new blob
                        session_data_bytes = json.dumps(frames).encode('utf-8')
                        blob_client.upload_blob(session_data_bytes)


    def get_name(self, sid):
        '''For session with id sid, return the name that should be used to identify
        this session in Azure blob storage.

        Args:   sid (str)  - the uuid of the session
        '''
        return f"session{sid}"


def temp_add_example_session():
    '''Session is owned by example user already inserted in the database.
    Run django admin site to see example user and session.'''
    json_dir = os.path.abspath("../data/static/data/")
    json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
    json_files.sort()

    session_store.populate(1)
    session_store = session_store.get()

    for i, json_file in enumerate(json_files):
        json_path = os.path.join(json_dir, json_file)
        
        with open(json_path, "r") as f:
            data = json.load(f)
            session_store[str(i + 1)] = data['keypoints3D']

    session_store.set(session_store)

    # This is the id of the session as defined in temp_add_example_user()
    session_store.write(1)
