'''
Created on 26 июня 2014 г.

@author: Andrean
'''
import core


class DataManager(object):
    def __init__(self):
        self._db    = core.getCoreInstance().getInstance('STORAGE').getInstance()
        
    def getDataItem(self, _id):
        
    
    def getData(self, _meta_id, _from, _to):
        pass