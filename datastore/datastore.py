import os
import json
from datetime import datetime
import uuid

users = {}
session = {}

class Datastore:
    def __init__(self):
        self.users = users
        self.session = session

    def get_users(self):
        return self.users

    def set_users(self, store):
        if not isinstance(store, dict):
            raise TypeError('store must be of type dictionary')
        self.users = store

    def populate_users(self):
        '''Reads data from user json file and add it to data store'''
        path = os.path.dirname(__file__)
        try:
            with open(path + "/users.json", "r") as f:
                self.users = json.loads(f.read())
        except:
            self.users = {}

    def write_users(self):
        '''Writes data from users data store to users json file'''
        path = os.path.dirname(__file__)
        with open(path + "/users.json", "w") as f:
            json.dump(self.users, f, indent=4)

    def get_session(self):
        return self.session

    def set_session(self, store):
        if not isinstance(store, dict):
            raise TypeError('store must be of type dictionary')
        self.session = store
    
    def populate_session(self, session_id):
        '''Populate session dict with the contents of a specific session file.
        Return true if session file already existed, false otherwise.

        Args:   session_file (str)  - the uuid of the session being searched         
        '''
        path = os.path.dirname(__file__)
        try:
            with open(path + "/sessions/session_" + session_id + ".json", "r") as f:
                self.session = json.loads(f.read())
            return True
        except:
            self.session = {}
            return False

    def write_session(self, session_id):
        '''Write contents of session data store to corresponding session json file

        Args:   session_file (str)  - the uuid of the session being written         
        '''
        path = os.path.dirname(__file__)
        with open(path + "/sessions/session_" + session_id + ".json", "w") as f:
            json.dump(self.session, f, indent=4)



# Some temporary functions for loading sample data into the data store
def temp_add_example_user():
    users_store = data_store.get_users()

    # use "1" for simplicity at this point, can switch later to using uuid
    users_store["1"] = {
        'first_name': "Jane",
        'last_name': "Doe",

        # a dict of sessions containing session metadata, indexed by session id
        # again, session id may be switched to uuid later
        'sessions': {
            "1": {
                "name": "my first session",
                "description": "some description",
                "date": "04/01/2023, 12:20:16",
            }
        }
    }
    data_store.set_users(users_store)
    data_store.write_users()


def temp_add_example_session():
    '''Session is owned by example user created above'''
    json_dir = os.path.abspath("data/static/data/")
    json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
    json_files.sort()

    data_store.populate_session("1")
    session_store = data_store.get_session()

    for i, json_file in enumerate(json_files):
        json_path = os.path.join(json_dir, json_file)
        
        with open(json_path, "r") as f:
            data = json.load(f)
            session_store[str(i + 1)] = data['keypoints3D']

    data_store.set_session(session_store)
    
    # This is the id of the session as defined in temp_add_example_user()
    data_store.write_session("1")


global data_store
data_store = Datastore()
data_store.populate_users()
#temp_add_example_session()
#temp_add_example_user()
