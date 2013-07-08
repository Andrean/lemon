'''
Created on 08.07.2013

@author: vau
'''
import threading
import queue
import uuid
import time
from collections import namedtuple

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
        self._taskTemplate  = {'__self': 0,'__id': None, 'state': STATE.STOPPED, 'exit_code': None, 'result': None}
        self._lock  = threading.Lock()
        threading.Thread.__init__(self)
        
    def run(self):
        pass
    
    def _process(self):
        self._running   = True
        while(self._running):
            if self._taskQueue.empty() is False:
                task    = self._taskQueue.get()
                self._tasks[task.id]  = self._taskTemplate
                self._tasks[task.id]['__id']    = task.id
                task.start(self._tasks[task.id])
            else:
                time.sleep(0.01)
            
        
    def add_task(self, _task):         
        self._taskQueue.put(_task)
        
    def new_task(self, _func):
        task    = Task(_func)
        self.add_task(task)
    
    def remove_task(self, task_id):
        self._tasks.pop(task_id) 
        
    def quit(self):
        self._running   = False
           
          
        
class Task(threading.Thread):
    
    def __init__(self, _func):
        self.id    = uuid.uuid4()
        self.func    = _func
        
    
    def run(self, tm):
        taskNote  = tm
        taskNote['__self']    = self
        taskNote['state']     = STATE.RUNNING
        try:
            print('i am task: {0}'.format(str(self.id)))
            taskNote['result'] = 1
            taskNote['exit_code'] = 0
        except Exception as e:
            taskNote['exit_code'] = 1
            taskNote['result'] = e 
        
        
        
        
        
        
        
        
        
        
        
