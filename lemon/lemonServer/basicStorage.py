'''
Created on 14.06.2013

@author: vau
'''

import common.IdGenerator
import threading

class Storage(threading.Thread):
    '''
    Class using different files for every item
    '''


    def __init__(self, preinitFile):
        '''
        Constructor
        '''
        self._storageID =   self._read(preinitFile)
        if(~self._storageID):                                        
            self._storageID = common.IdGenerator.GenerateNewUniqueID();
            self._write(preinitFile, self._storageID)
        threading.Thread.__init__(self)
        self._lock  = threading.Lock()    
        
    # return byte content from file
    def readItem(self, item_id):
        fileName = self._getFilename(item_id);
        return self._read(fileName);
    
    # transform content to byte sequence and write it into file
    def writeItem(self, item_id, content):
        fileName = self._getFilename(item_id);
        return self._write(fileName, content);
    
    def _read(self, file):
        self._lock()
        try:
            f = open(file, 'rb');
        except IOError:
            return;
        content = f.read()
        f.close()
        self._unlock()
        return content
    
    def _write(self, file, content):
        self._lock()
        f = open(file, 'wb')
        f.write(content)
        self._unlock()
            
    def _getFilename(self, item_id):
        if not item_id:
            return self._storageID + item_id;
        
    def _lock(self):
        self._lock.acquire()
        
    def _unlock(self):
        self._lock.release()