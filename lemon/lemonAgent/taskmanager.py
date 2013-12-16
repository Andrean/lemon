'''
Created on 08.07.2013

@author: vau
'''
import threading
import queue
import uuid
import time
from collections import namedtuple
import tasks
import lemon
import core
import lemon_threadpool

_state   = namedtuple('STATE',['INIT','RUNNING','STOPPED'])

STATE   = _state(0, 1 , 2)

TASK_COMMANDS   = namedtuple('TASK_COMMANDS',['GET_COUNTER', 'STORE', 'SEND', 'RECV', 'CHECK'])


class TaskManager(lemon.BaseAgentLemon):
    '''
    classdocs
    '''

    def __init__(self, _logger, _config, _info):
        self._taskQueue = queue.Queue()
        self._tasks     = {}
        self._taskTemplate  = {'__self': 0, '__id': None, 'state': STATE.STOPPED, 'exit_code': None, 'result': None}
        self._lock  = threading.Lock()
        self._pool  = lemon_threadpool.ThreadPool(15)
        self.taskmanagerInstance    = self
        
        lemon.BaseAgentLemon.__init__(self, _logger, _config, _info)
        
    def run(self):
        c   =   core.getCoreInstance()
        self.storageInstance        = c.getInstance('STORAGE')
        self.interfaceInstance      = c.getInstance('INTERFACE')
        self.contractorLayer        = c.getInstance('CONTRACTOR')
        self.scheduler              = c.getInstance('SCHEDULER')
        self.agentID                = c.getItem('agent')['__id']
        self._pool.start()
        
        self._setReady()
        self._logger.info('Task Manager started')
        while self._running:
            self._process()
        self._pool.quit()
        self._logger.info('Shutdown ThreadPool')
        self._logger.info('Task Manager shutdown')    
        
    
    def _process(self):
        try:
            task    = self._taskQueue.get(True, 5)
            #self._logger.debug('Trying to start task {0}'.format(task.id))
            self._pool.put(task)
            #task.start()
        except queue.Empty:
            return        
        
    def add_task(self, _task): 
        self._taskQueue.put(_task)
        
    def new_task(self, _func, **kwargs):
        _id                          = uuid.uuid4()
        self._tasks[_id]             = self._taskTemplate
        self._tasks[_id]['__id']     = _id
        if type(_func) is str:
            self.add_task( Task(_id, self._tasks[_id], self._logger, self, tasks.CMD[_func], **kwargs) )
        elif hasattr(_func, '__call__'):
            self.add_task( Task(_id, self._tasks[_id], self._logger, self, _func, **kwargs) )
        else:
            raise NotTaskException
        #self._logger.debug('Adding new task into queue. Task id {0}'.format(_id))
    
    def remove_task(self, task_id):
        self._tasks.pop(task_id) 
        self._logger.debug('Task {0} successfully removed '.format(task_id))       
          
        
class Task(object):
    
    def __init__(self, _id ,_tm, _logger, _parent, _func, **kwargs):
        self.id    = _id
        self.func  = _func
        self.tm    = _tm
        self._parent   = _parent
        self.kwargs = kwargs
        self._logger    = _logger
    
    def run(self):
        logger      = self._logger
        taskNote    = self.tm
        taskNote['__self']    = self
        taskNote['state']     = STATE.RUNNING
        try:
            if self.kwargs:
                self.func(self, **(self.kwargs))
            else:
                self.func(self)
            
            #logger.debug('task {0} started'.format(self.id))
            #print('i am task: {0}'.format(str(self.id)))
            taskNote['result'] = 1
            taskNote['exit_code'] = 0
        except Exception as e:
            logger.error('Error occured in task {0}: {1}'.format(self.id, str(e)))
            logger.exception(e)
            taskNote['exit_code'] = 1
            taskNote['result'] = e
    
class NotTaskException(ValueError):
    pass