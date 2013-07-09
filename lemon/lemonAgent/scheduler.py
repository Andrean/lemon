'''
Created on 08.07.2013

@author: vau
'''
import threading
import time
import json
import uuid

MASK    = 'schedule_'
MAIN    = 'items'

CHECK_INTERVAL  = 0.1
STORE_INTERVAL  = 1

SECONDS = 1
MINUTES = 60*SECONDS
HOURS   = 60*MINUTES
DAYS    = 24*HOURS


class Scheduler(threading.Thread):
    '''
    classdocs
    '''


    def __init__(self, _logger, _config, _storageInstance, _taskmanagerInstance):
        '''
        Constructor
        '''
        self._logger    = _logger
        self._config    = _config
        self._storage   = _storageInstance
        self._taskManager   = _taskmanagerInstance
        self._schedule  = {}
        self._scheduleModified  = False
        self._running   = False
        threading.Thread.__init__(self)
        
    def run(self):
        self._logger.info('Scheduler started')
        self._loadStorage()
        self._running   = True
        it  = 0
        while self._running:
            self._process()
            time.sleep(CHECK_INTERVAL)
            it += CHECK_INTERVAL
            if it > STORE_INTERVAL :
                it = 0
                self._store_schedule()
            
    def waitReady(self):
        while self._running is not True:
            time.sleep(0.1)
            
    def add(self, func_type, name='default', start_time=None, interval = 5*MINUTES,  kwargs=None):
        schtask = {}
        if start_time is None:
            start_time  = time.time()
        schtask['__id'] = str(uuid.uuid4())
        schtask['name'] = name
        schtask['start_time']   = start_time
        schtask['last_time']    = start_time
        schtask['interval']     = interval
        schtask['task']         = {'func': func_type, 'args': kwargs}
        self._add_to_schedule(schtask['__id'], schtask)
        self._store(schtask['__id'], schtask)

    def _add_to_schedule(self, _key, _schtask):
        self._schedule[_key] = _schtask
        self._scheduleModified  = True        
        
    def _store(self, key, obj):
        try:
            self._storage.writeItem(MASK + str(key), json.dumps(obj))
            self._store_schedule()              
        except Exception as e:
            self._logger.error('Error occured in _store while storing {0}: {1}'.format(str(key), str(e)))
    
    def _loadStorage(self):
        try: 
            items   = self._storage.readStr(MASK + MAIN)
            if items is not None:
                headers   = json.loads(items)
                for key in headers:
                    item    = json.loads(self._storage.readStr(MASK + key))
                    self._add_to_schedule(key, item)
                self._logger.info('schedule loaded')
        except Exception as e:
            self._logger.error('Error occured in _loadStorage: {0}'.format(str(e)))
            
    def _process(self):
        timestamp   = time.time()
        keys    = list(self._schedule.keys())
        for k in keys:
            if self._schedule[k]['last_time'] + self._schedule[k]['interval'] < timestamp:
                self._schedule[k]['last_time']  = time.time()
                self._startTask(k, self._schedule[k]['task'])
                self._logger.info('scheduled task {0} started'.format(str(k)))
                
    def _store_schedule(self):
        if self._scheduleModified:
            self._storage.writeItem(MASK + MAIN, json.dumps(list(self._schedule.keys())))
            self._scheduleModified = False
                
    def _startTask(self, key, task):
        self._taskManager.new_task(task['func'], task['args'])
        self._logger.info('task {0} successfully send to task manager'.format(str(key)))
    
    
    def quit(self):
        self._running   = False