import os
import orjson
import json
import datastore.const as const
from azure.storage.blob import BlobServiceClient

class Sessionstore:
    def __init__(self):
        self.session = {}

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

    def write_local(self, sid):
        ''' KEEP VERSION FOR LOCAL STORAGE UNTIL BLOB STORAGE FINALISED'''
        path = os.path.dirname(__file__)
        with open(path + "/sessions/session_" + str(sid) + ".json", "w") as f:
            json.dump(self.session, f, indent=4)

    def write(self, sid):
        '''If Azure blob exists for this session, append current session data to this blob.
        Otherwise, create a new blob for this session and store session data in new blob.

        Args:   sid (str)  - the uuid of the session being written         
        '''
        # Create a blob client 
        blob_service_client = BlobServiceClient.from_connection_string(const.AZ_CON_STR)
        blob_client = blob_service_client.get_blob_client(const.AZ_CONTAINER_NAME, self.get_name(sid))

        # Upload the session data.
        # if blob under that sessionId exists, append frames
        if blob_client.exists():
            # Download the existing session data 
            downloaded_bytes = blob_client.download_blob().readall()
            existing_data = json.loads(downloaded_bytes)

            # Append the new frame to the existing session data
            existing_data.update(self.session)
            updated_session_data_bytes = json.dumps(existing_data).encode('utf-8')

            # Upload the updated session data (overwrite with updated information)
            blob_client.upload_blob(updated_session_data_bytes, overwrite=True)
        else:
            # If the sessionId does not exist, upload the session data as a new blob
            session_data_bytes = json.dumps(self.session).encode('utf-8')
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
