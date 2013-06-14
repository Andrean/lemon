'''
Created on 14.06.2013

@author: vau
'''

class Storage(object):
    '''
    Class using different files for every item
    '''


    def __init__(self, _uniqueId):
        '''
        Constructor
        '''
        self._storageID = _uniqueId;
    def readItem(self, item_id):
        pass
    
    def writeItem(self, item_id, content):
        pass
    
    def _read(self, file):
        pass
    
    def _write(self, file, content):
        pass
    