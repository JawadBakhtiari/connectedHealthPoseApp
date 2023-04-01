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


global data_store
data_store = Datastore()
data_store.populate_data()
