'''
Created on 08.07.2013

@author: vau
'''
import threading
import queue
import uuid
import time
from collections import namedtuple
import task_templates

_state   = namedtuple('STATE',['INIT','RUNNING','STOPPED'])

STATE   = _state(0, 1 , 2)

TASK_COMMANDS   = namedtuple('TASK_COMMANDS',['GET_COUNTER', 'STORE', 'SEND', 'RECV', 'CHECK'])


class TaskManager(threading.Thread):
    '''
    classdocs
    '''

    def __init__(self, _logger, _config):
        self._logger    = _logger
        self._config    = _config
        self._taskQueue = queue.Queue()
        self._tasks     = {}
        self._taskTemplate  = {'__self': 0, '__id': None, 'state': STATE.STOPPED, 'exit_code': None, 'result': None}
        self._lock  = threading.Lock()
        self.storageInstance    =   None
        self.interfaceInstance  =   None
        self.taskmanagerInstance    = self
        self.contractorLayer        = None
        self.scheduler              = None
        threading.Thread.__init__(self)
        
    def run(self):
        self._running   = True
        self._logger.info('Task Manager started')
        while self._running:
            self._process()
        self._logger.info('Task Manager shutdown')    
        
    
    def _process(self):
        if self._taskQueue.empty() is False:
            task    = self._taskQueue.get()
            self._logger.debug('Trying to start task {0}'.format(task.id))
            task.start()
        else:
            time.sleep(0.01)
        
        
    def add_task(self, _task):         
        self._taskQueue.put(_task)
        
    def new_task(self, _func, kwargs=None):
        _id                          = uuid.uuid4()
        self._tasks[_id]             = self._taskTemplate
        self._tasks[_id]['__id']     = _id
        task                        = Task(_id, self._tasks[_id], self._logger, self, task_templates.CMD[_func], kwargs)
        self._logger.debug('Adding new task into queue. Task id {0}'.format(_id))
        self.add_task(task)
    
    def remove_task(self, task_id):
        self._tasks.pop(task_id) 
        self._logger.debug('Task {0} successfully removed '.format(task_id))
        
    def quit(self):
        self._running   = False
           
          
        
class Task(threading.Thread):
    
    def __init__(self, _id ,_tm, _logger, _parent, _func, kwargs):
        self.id    = _id
        self.func  = _func
        self.tm    = _tm
        self._parent   = _parent
        self.kwargs = kwargs
        self._logger    = _logger
        threading.Thread.__init__(self)
        
    
    def run(self):
        logger      = self._logger
        taskNote    = self.tm
        taskNote['__self']    = self
        taskNote['state']     = STATE.RUNNING
        try:
            self.func(self, self.kwargs)
            logger.info('task {0} started'.format(self.id))
            #print('i am task: {0}'.format(str(self.id)))
            taskNote['result'] = 1
            taskNote['exit_code'] = 0
        except Exception as e:
            logger.error('Error occured in task {0}: {1}'.format(self.id, str(e)))
            taskNote['exit_code'] = 1
            taskNote['result'] = e 
        
        
        
        
        
        
        
        
        
        
        
