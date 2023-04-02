import os
import json
from datetime import datetime

users = {}

class Datastore:
    def __init__(self):
        self.__store = users

    def get(self):
        return self.__store
    
    def set(self, store):
        if not isinstance(store, dict):
            raise TypeError('store must be of type dictionary')
        self.__store = store

    def populate_data(self):
        '''Reads data from datastore.json and adds it to data store'''
        path = os.path.dirname(__file__)

        with open(path + "/datastore.json", "r") as f:
            self.__store = json.loads(f.read())

    def write_data(self):
        '''Writes data from data store into datastore.json'''
        path = os.path.dirname(__file__)

        with open(path + "/datastore.json", "w") as f:
            json.dump(self.__store, f, indent=4)


def temp_add_example_frames():
    '''A temporary function for adding example frames during testing'''
    json_dir = os.path.abspath("data/static/data/")
    json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
    json_files.sort()

    store = data_store.get()
    store["1"]["sessions"]["1"]["frames"] = {}
    for i, json_file in enumerate(json_files):
        json_path = os.path.join(json_dir, json_file)
        
        with open(json_path, "r") as f:
            data = json.load(f)
            store["1"]["sessions"]["1"]["frames"][str(i + 1)] = data['keypoints3D']
    data_store.set(store)
    data_store.write_data()


global data_store
data_store = Datastore()
data_store.populate_data()
