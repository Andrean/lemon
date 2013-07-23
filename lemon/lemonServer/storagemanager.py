'''
Created on 21.06.2013

@author: vau
'''

import uuid
import storage
import time
import lemon
import exception.lemonException as le


GARBAGE_INTERVAL    = 200 # 100 секунд проверка пула стораджей на то , что они используются
TIME_NOT_USED       = 20

class StorageManager(lemon.BaseServerComponent):
    
    def __init__(self, _logger, _cfg, _info):
        self._storagePool  = []
        lemon.BaseServerComponent.__init__(self, _logger, _cfg, _info)    
            
    def run(self):
        self._setReady()
        last_clean  = time.time()
        self._logger.info('storage manager started')
        while self._running:
            time.sleep(0.1)
            if last_clean + GARBAGE_INTERVAL < time.time():
                last_clean  = time.time()
                self.cleanStoragePool()
            
    def cleanStoragePool(self):
        self._removed_list  = []
        for i, st_info in enumerate(self._storagePool):
            if st_info['last_used_time'] + TIME_NOT_USED  < time.time():
                st_info['instance'].quit()
                self._removed_list.append(i)
        print("CLEANING STORAGE POOL. {0} WILL BE DELETED".format(str(len(self._removed_list))))
        if len(self._removed_list) > 0:
            self._removed_list.reverse()
            for i in self._removed_list:
                self._storagePool.pop(i)
            
    def _getNonUsedInstance(self):
        for st_info in self._storagePool:
            if st_info['last_used_time'] + TIME_NOT_USED  < time.time():
                st_info['last_used_time'] = time.time()
                return st_info
        
    def getInstance(self):
        try:
            st  = self._getNonUsedInstance()
            print("GETTING " + str(st))
            if st is not None:
                st['instance'].set_default_collection(None)
                print('USING NOT USED STORAGE INSTANCE')
                return st['instance']
            st  = {'id': uuid.uuid4(), 'name': 'storage_instance','state': 'noninit', '_': None, 'last_used_time': None};
            stInstance  = storage.Storage(self._logger, self._config, st )
            stInstance.start()
            self._info['threads']+= 1
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