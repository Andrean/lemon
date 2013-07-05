'''
Created on 21.06.2013

@author: vau
'''

import uuid
import storage
import time

class StorageManager():
    
    def __init__(self, logger, cfg):
        '''
        Constructor
        '''
        self._storagePool  = []
        self._logger    = logger
        self._config    = cfg    
            
    def getInstance(self):
        try:
            stInstance  = storage.Storage(self._logger, self._config)
            st  = {'id': uuid.uuid4(), 'status': 'running', '_': stInstance};
            stInstance.start()
            self._storagePool.append(st);
            return stInstance, st['id']
        except Exception as e:
            self._logger("Exception while starting new storage instance with id '{0}': {1}".format(st['id']), str(e))
    
    def stopInstance(self, _id):
        for instance in self._storagePool:
            if instance['id'] == _id:
                instance['_'].stop()
                instance['status'] = 'stopped'       
                
      
    def quit(self):
        self._running  = False;