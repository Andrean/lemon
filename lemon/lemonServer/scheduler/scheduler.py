'''
Created on 23.07.2013

@author: vau
'''
import time
import uuid
import lemon
import core
import scheduler.tasks

#import scheduler.default_tasks as tasks

CHECK_INTERVAL  = 0.1
STORE_INTERVAL  = 1

SECONDS = 1
MINUTES = 60*SECONDS
HOURS   = 60*MINUTES
DAYS    = 24*HOURS


class Scheduler(lemon.BaseServerComponent):

    def __init__(self, _logger, _config, _info):
        '''
        Constructor
        '''
        self._storage   = None
        self._taskManager   = None
        self._schedule  = {}
        self._removed_from_schedule = []
        self._scheduleModified  = False
        lemon.BaseServerComponent.__init__(self, _logger, _config, _info)
        
    def run(self):
        
        self._sm        = core.getCoreInstance().getInstance('STORAGE')
        self._storage   = self._sm.getInstance()
        self._storage.set_default_collection('scheduler')
        self._taskManager   = core.getCoreInstance().getInstance('TASK_MANAGER')
        self._logger.info('Scheduler started')
        
        self._loadStorage()
        self._setReady()
        self.loadDefaultTasks()
        it  = 0
        while self._running:
            self._process()
            time.sleep(CHECK_INTERVAL)
            it += CHECK_INTERVAL
            if it > STORE_INTERVAL :
                it = 0
                self._store_schedule()
        self._logger.info('stop SCHEDULER')
    
    def loadDefaultTasks(self):
        default_tasks   = scheduler.tasks.CMD
        for task in default_tasks:
            self._taskManager.addTask('addScheduledTask', task)   
            
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
        
    def getScheduledTask(self, name):
        for v in self._schedule.values():
            if v['name']    == name:
                return v
    '''        
    def getNotInitiatedDefaultTasks(self):
        for taskName, task in tasks.tasks.items():
            if self.getScheduledTask(taskName) is None:
                yield task
    '''
    def _add_to_schedule(self, _key, _schtask):
        self._schedule[_key] = _schtask
        self._scheduleModified  = True  
        
    def _remove_from_schedule(self, _key): 
        self._schedule.pop(_key)
        self._removed_from_schedule.append(_key)     
        
    def _store(self, key, obj):
        try:
            q       = {'name': key}
            storing = {'name': key, 'task': obj}
            item    = self._storage.findOne(q)
            if item:
                self._storage.update(q, storing)
            else:
                self._storage.insert(storing)
            self._store_schedule()              
        except Exception as e:
            self._logger.error('Error occured in _store while storing {0}: {1}'.format(str(key), str(e)))
    
    def _loadStorage(self):
        try: 
            items   = self._storage.findOne({'type': 'task_list'})
            print(items)
            if items is not None:
                headers   = items['list']
                for key in headers:
                    item    = self._storage.findOne({'name': key})
                    self._add_to_schedule(key, item['task'])
            else:
                self._storage.insert({'type': 'task_list', 'list': []})            
        except Exception as e:
            self._logger.error('Error occured in _loadStorage: {0}'.format(str(e)))
            
    def _process(self):
        timestamp   = time.time()
        keys    = list(self._schedule.keys())
        remove_list = []
        for k in keys:
            if self._schedule[k]['interval'] == 0:
                self._startTask(k, self._schedule[k]['task'])
                remove_list.append(k)
            elif self._schedule[k]['last_time'] + self._schedule[k]['interval'] < timestamp:
                self._startTask(k, self._schedule[k]['task'])
                self._schedule[k]['last_time']  = time.time()
        for remove_name in remove_list:
            self._remove_from_schedule(remove_name)
                
                
    def _store_schedule(self):
        if self._scheduleModified:
            q   = {'type': 'task_list'}
            doc = {'type': 'task_list', 'list': list(self._schedule.keys())}
            self._storage.update(q, doc)
            for key in self._removed_from_schedule:
                self._storage.remove({'name': key})
            self._removed_from_schedule = []
            self._scheduleModified = False
                
    def _startTask(self, key, task):
        self._taskManager.addTask(task['func'], task['args'])        