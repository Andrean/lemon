'''
Created on 14 июля 2014 г.

@author: Andrean
'''
import core
import bson

class Base(object):
    '''
    classdocs
    '''    
    def __init__(self, dbref, collection, data):
        self.__dbref = dbref
        self.__data  = data
        self.__collection = collection
    
    def Data(self):
        return self.__data
    
    def set(self, value):
        for k,v in value.items():
            self.__data[k] = v
    
    def load(self):
        storage = core.getCoreInstance().getInstance('STORAGE').getInstance()        
        self.__data = storage.db.dereference(self.__dbref)
        
    def save(self):
        to_save = self.__data
        for k,v in to_save.items():
            if isinstance(v, Base) and hasattr(v,"__dbref"):
                to_save[k] = v.__dbref
        storage = core.getCoreInstance().getInstance('STORAGE').getInstance()
        storage.set_default_collection(self.__collection)
        storage.save(to_save)
    
    def populate(self):
        storage = core.getCoreInstance().getInstance('STORAGE').getInstance()        
        for k, v in self.__data.items():
            if isinstance(v, bson.DBRef):
                value = storage.db.dereference(v)
                value.__dbref = v
                self._data[k] = value      
        
class ItemNotFoundException(Exception):
    pass