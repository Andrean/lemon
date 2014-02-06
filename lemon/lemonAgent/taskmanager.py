'''
Created on 08.07.2013

@author: vau
'''
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

QUEUE_FULL_WAIT_INTERVAL    = 10


class TaskManager(lemon.BaseAgentLemon):
    '''
    classdocs
    '''

    def __init__(self, _logger, _config, _info):
        self._taskQueue = queue.Queue()
        self._tasks     = {}
        self._taskTemplate  = {'__self': 0, '__id': None, 'state': STATE.STOPPED, 'exit_code': None, 'result': None}
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
            self._pool.put(task)            
        except queue.Empty:
            return  
        except queue.Full:
            time.sleep(QUEUE_FULL_WAIT_INTERVAL)
            self._logger.warn('ThreadPool Queue is full. Waiting {0} seconds'.format(str(QUEUE_FULL_WAIT_INTERVAL)))
        
    def add_task(self, _task): 
        self._taskQueue.put(_task)
        
    def new_task(self, _func, **kwargs):
        _id                          = uuid.uuid4()
        if type(_func) is str:
            self.add_task( Task(_id, self._logger, self, tasks.CMD[_func], **kwargs) )
        elif hasattr(_func, '__call__'):
            self.add_task( Task(_id, self._logger, self, _func, **kwargs) )
        else:
            raise NotTaskException
        
    def remove_task(self, task_id):
        self._tasks.pop(task_id) 
        self._logger.debug('Task {0} successfully removed '.format(task_id))       
          
        
class Task(object):
    
    def __init__(self, _id , _logger, _parent, _func, **kwargs):
        self.id    = _id
        self.func  = _func
        self._parent   = _parent
        self.kwargs = kwargs
        self._logger    = _logger
    
    def run(self):
        logger      = self._logger
        try:
            if self.kwargs:
                self.func(self, **(self.kwargs))
            else:
                self.func(self)
        except Exception as e:
            logger.error('Error occured in task {0}: {1}'.format(self.id, str(e)))
            logger.exception(e)
                    
class NotTaskException(ValueError):
    pass