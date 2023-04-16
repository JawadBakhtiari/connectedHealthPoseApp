import os
import orjson
import json

session = {}

class Sessionstore:
    def __init__(self):
        self.session = session

    def get(self):
        return self.session

    def set(self, store):
        if not isinstance(store, dict):
            raise TypeError('store must be of type dictionary')
        self.session = store
    
    def populate(self, session_id):
        '''Populate session dict with the contents of a specific session file.
        Return true if session file already existed, false otherwise.

        Args:   session_file (str)  - the uuid of the session being searched         
        '''
        path = os.path.dirname(__file__)
        try:
            with open(path + "/sessions/session_" + str(session_id) + ".json", "r") as f:
                self.session = orjson.loads(f.read())
            return True
        except FileNotFoundError:
            self.session = {}
            return False

    def write(self, session_id):
        '''Write contents of session data store to corresponding session json file

        Args:   session_file (str)  - the uuid of the session being written         
        '''
        path = os.path.dirname(__file__)
        with open(path + "/sessions/session_" + str(session_id) + ".json", "w") as f:
            json.dump(self.session, f, indent=4)


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
