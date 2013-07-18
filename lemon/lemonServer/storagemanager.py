'''
Created on 21.06.2013

@author: vau
'''

import uuid
import storage
import time
import lemon
import exception.lemonException as le

class StorageManager(lemon.BaseServerComponent):
    
    def __init__(self, _logger, _cfg, _info):
        self._storagePool  = []
        lemon.BaseServerComponent.__init__(self, _logger, _cfg, _info)    
            
    def run(self):
        self._setReady()
        self._logger.info('storage manager started')
        while self._running:
            time.sleep(0.1)
            
    def getInstance(self):
        try:
            stInstance  = storage.Storage(self._logger, self._config)
            st  = {'id': uuid.uuid4(), 'status': 'running', '_': stInstance};
            stInstance.start()
            self._storagePool.append(st);
            return stInstance
        except le.StorageNotCreatedException as e:
            self._logger.exception(e)
    
    def stopInstance(self, _id):
        for instance in self._storagePool:
            if instance['id'] == _id:
                instance['_'].stop()
                instance['status'] = 'stopped'       
                
      
    def quit(self):
        self._running  = False;