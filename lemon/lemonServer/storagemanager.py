'''
Created on 21.06.2013

@author: vau
'''

import uuid
import storage
import time
import lemon
import queue
import exception.lemonException as le


TIME_NOT_USED       = 20

class StorageManager(lemon.BaseServerComponent):
    
    def __init__(self, _logger, _cfg, _info):
        lemon.BaseServerComponent.__init__(self, _logger, _cfg, _info)
        self._storagePool   = []
        self._taskQueue     = queue.Queue()
            
            
    def run(self):
        
        self.createStoragePool()
        self._setReady()
        self._logger.info('storage manager started')
        while self._running:
            time.sleep(0.01)
            for k in self._storagePool:
                self._process(k['instance'])
            
    def createStoragePool(self, _size = 10):
        for _ in range(1,_size):
            st  = {'id': uuid.uuid4(), 'name': 'storage_instance','state': 'noninit', '_': None, 'last_used_time': None};
            instance  = storage.Storage(self._logger, self._config, st)
            instance.start()
            self._info['threads'] += 1
            self._storagePool.append(st)            
        
    def getInstance(self):
        try:            
            st  = StorageGhost(self)
            return st            
        except le.StorageNotCreatedException as e:
            self._logger.exception(e)
    
    def stopInstance(self, _id):
        for instance in self._storagePool:
            if instance['id'] == _id:
                instance['instance'].stop()
                instance['status'] = 'stopped'       
    
    def put(self, db_request):
        self._taskQueue.put(db_request)
        
    def _process(self, storageInstance):
        req     = self._taskQueue.get()
        method  = req['method']
        args    = req['args']
        cb      = req['callback']
        res     = storageInstance.do(method, *args)
        cb(res)
        
    
 
class   StorageGhost(object):
    def __init__(self, _storageManagerInstance):
        self._sm    = _storageManagerInstance
        self._collection    = None
        
    def _doREQUEST(self, method, *args):
        res     = {'result': None, 'done': False}
        def callback(response):
            res['result']   = response
            res['done']     = True
        req     = {'method': method,'args': args, 'callback': callback}
        self._sm.put(req)
        while res['done'] is not True:
            time.sleep(0.01)
        return res['result']
    
    def set_default_collection(self, collection):
        self._collection    = collection
    
    def update(self, query, doc):
        return self._doREQUEST('update', query, doc, self._collection)
        
    def insert(self, doc):
        return self._doREQUEST('insert', doc, self._collection)
    
    def remove(self, query):
        return self._doREQUEST('remove', query, self._collection)
    
    def find(self, query):
        return self._doREQUEST('find', query, self._collection)
    
    def findOne(self, query):
        return self._doREQUEST('findOne', query, self._collection)
    
    