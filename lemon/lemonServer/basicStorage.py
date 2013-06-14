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
        self._lock  = threading.Lock()
        self._storageID =   self._read(preinitFile) or ''
        if  self._storageID is '':                                        
            self._storageID = common.IdGenerator.GenerateNewUniqueID();
            self._write(preinitFile, self._storageID)
        else:
            self._storageID = str(self._storageID, 'utf-8')
        threading.Thread.__init__(self)
         
        
    def run(self):
        print(self._storageID)
        
    # return byte content from file
    def readItem(self, item_id):
        fileName = self._getFilename(item_id);
        return self._read(fileName);
    
    # transform content to byte sequence and write it into file
    def writeItem(self, item_id, content):
        fileName = self._getFilename(item_id);
        return self._write(fileName, content);
    
    def _read(self, file):
        self._dolock()
        try:
            f = open(file, 'rb');
        except IOError:
            self._unlock()
            return;
        content = f.read()
        f.close()
        self._unlock()
        return content
    
    def _write(self, file, content):
        self._dolock()
        f = open(file, 'wb')
        f.write(bytes(content, 'utf-8'))
        f.close()
        self._unlock()
            
    def _getFilename(self, item_id):
        if not item_id:
            return self._storageID + item_id;
        
    def _dolock(self):
        self._lock.acquire()
        
    def _unlock(self):
        self._lock.release()