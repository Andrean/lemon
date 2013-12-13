'''
Created on 08.07.2013

@author: vau
'''
import time
import json
import uuid
import lemon
import core
import scheduler.default_tasks as tasks

MASK    = 'schedule_'
MAIN    = 'items'

CHECK_INTERVAL  = 0.1
STORE_INTERVAL  = 1

SECONDS = 1
MINUTES = 60*SECONDS
HOURS   = 60*MINUTES
DAYS    = 24*HOURS


class Scheduler(lemon.BaseAgentLemon):
    '''
    classdocs
    '''


    def __init__(self, _logger, _config, _info):
        '''
        Constructor
        '''
        self._storage   = None
        self._taskManager   = None
        self._schedule  = {}
        self._removed_from_schedule = []
        self._scheduleModified  = False
        lemon.BaseAgentLemon.__init__(self, _logger, _config, _info)
        
    def run(self):
        
        self._storage       = core.getCoreInstance().getInstance('STORAGE')
        self._taskManager   = core.getCoreInstance().getInstance('TASK_MANAGER')
        self._logger.info('Scheduler started')
        self._loadStorage()
        self._setReady()
        it  = 0
        while self._running:
            self._process()
            time.sleep(CHECK_INTERVAL)
            it += CHECK_INTERVAL
            if it > STORE_INTERVAL :
                it = 0
                self._store_schedule()
        self._logger.info('Shutdown scheduler')
            
    def add(self, func_type, name='default', start_time=None, interval = 5*MINUTES,  kwargs=None, revision=0):
        schtask = {}
        if start_time is None:
            start_time  = time.time()
        schtask['__id'] = str(uuid.uuid4())
        schtask['name'] = name
        schtask['start_time']   = start_time
        schtask['last_time']    = start_time - interval
        schtask['interval']     = interval
        schtask['task']         = {'func': func_type, 'args': kwargs}
        schtask['__revision']   = revision
        self._add_to_schedule(schtask['__id'], schtask)
        self._store(schtask['__id'], schtask)
        
    def remove(self, name):
        removed = None
        for k, v in self._schedule.items():
            if v['name'] == name:
                print("REMOVING: "+str(v['name']))
                removed = k
        if removed:
            self._remove_from_schedule(removed)
        
    def getScheduledTask(self, name=None):
        if name is None:
            return self._schedule
        for v in self._schedule.values():
            if v['name']    == name:
                return v
            
    def getSchedule(self):
        for v in self._schedule.values():
            yield v
            
    def getNotInitiatedDefaultTasks(self):
        for taskName, task in tasks.tasks.items():
            if self.getScheduledTask(taskName) is None:
                yield task

    def _add_to_schedule(self, _key, _schtask):
        self._schedule[_key] = _schtask
        self._scheduleModified  = True  
        
    def _remove_from_schedule(self, _key): 
        self._schedule.pop(_key)
        self._removed_from_schedule.append(_key)     
        
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
        remove_list = []
        for k in keys:
            if self._schedule[k]['interval'] == 0:
                self._startTask(k, self._schedule[k]['task'])
                self._logger.info('scheduled task {0} started'.format(str(k)))
                remove_list.append(k)
            elif self._schedule[k]['last_time'] + self._schedule[k]['interval'] < timestamp:
                self._startTask(k, self._schedule[k]['task'])
                self._logger.info('scheduled task {0} started'.format(str(k)))
                self._schedule[k]['last_time']  = time.time()
        for remove_name in remove_list:
            self._remove_from_schedule(remove_name)
                
                
    def _store_schedule(self):
        if self._scheduleModified:
            self._storage.writeItem(MASK + MAIN, json.dumps(list(self._schedule.keys())))
            for key in self._removed_from_schedule:
                self._storage.deleteItem(MASK+key)
            self._removed_from_schedule = []
            self._scheduleModified = False
                
    def _startTask(self, key, task):
        self._taskManager.new_task(task['func'], task['args'])
        self._logger.info('task {0} successfully send to task manager'.format(str(key)))
