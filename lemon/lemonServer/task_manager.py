'''
Created on 21.06.2013

@author: vau
'''

import threading 
import queue
import uuid
import time
import exception.lemonException as lemonException
import tasks
import sys
import lemon
import core

def synchronized(f):
    '''Synchronization method decorator.'''

    def new_function(self, *args, **kwargs):
        self._lock.acquire()
        try:
            return f(self, *args, **kwargs)
        finally:
            self._lock.release()
    return new_function

class TaskManager(lemon.BaseServerComponent):
    '''
    This manager manage task: read, write, add content and other
    '''


    def __init__(self, _logger, _config, _info):
        self._TaskQueue = queue.Queue()
        self._lock  = threading.Lock()
        self._handlerList   = {}
        lemon.BaseServerComponent.__init__(self, _logger, _config, _info)
        
    def run(self):
        cr      = core.getCoreInstance()
        self._storageManager     = cr.getInstance('STORAGE')
        self._scheduler          = cr.getInstance('SCHEDULER')
        self._setReady()
        self._logger.info("Task manager started")
        while(self._running):
            self._process()            
        self._logger.info('Task Manager was successfully shutdown')
    
    def addTask(self, proc, *args):
        taskId  = str(uuid.uuid4())
        timestamp   = time.time()
        task    = {'id': taskId, 'start_timestamp': timestamp, 'end_timestamp': None, 'proc': proc, 'args' : args}
        self._addTask(task)
        
    def connectHandler(self, _handler):
        if _handler.getName() in self._handlerList.keys():
            raise lemonException.HandlerAlreadyInListException()
        else:
            self._handlerList[_handler.getName()] = _handler
            _handler._taskmanager   = self
            self._logger.debug('Handler %s connected' % _handler.getName())
            
    def shutdown(self):
        self._logger.info('Attempting to shutdown TaskManager')
        self._running   = False
        
    def _process(self):        
        try:
            task = self._TaskQueue.get(timeout=1)
            taskId = task['id']        
            self._logger.debug("Task=\"{0}\" taskId={1} is processed".format(task['proc'],taskId))
            for taskHandler in self._handlerList.values():
                taskHandler.do(task)
            self._logger.debug("Task=\"{0}\" taskId={1} was processed without errors".format(task['proc'],taskId))
        except queue.Empty:
            return
        except Exception as e:
            self._logger.error("Task=\"{0}\" taskId={1} was processed with error: {1}".format(task['proc'], taskId, str(e)))
            
    def _checkForTasks(self):
        if self._TaskQueue.empty():
            return False
        return True
    
    @synchronized
    def _addTask(self, task):
        try:
            self._TaskQueue.put(task)
        except Exception as ex:
            self._logger.exception(ex)
        
        
class BaseTaskHandler(object):
    
    def __init__(self, _name):
        self._taskmanager  = None
        self._name  = _name
        self._commandList   = []
        
    def getName(self):
        return self._name
    
    def do(self, task):
        task_cmd = task['proc']
        if task_cmd in self._commandList:
            try:
                self._dispatchMethod(task_cmd, task)
            except:
                self._taskmanager._logger.exception('Exception in task cmd '+ task_cmd, sys.exc_info()[1])
    
    def _dispatchMethod(self, cmd, task):
        args    = task['args']
        if cmd in self._commandList:
            tasks.CMD[cmd](self._taskmanager, *args)
    
class StoreTaskHandler(BaseTaskHandler):
    
    def __init__(self, name):
        BaseTaskHandler.__init__(self, name)
        self._commandList = ['storeAgentData', 'storeData', 'storeCurrentData']
    
    def _dispatchMethod(self, cmd, task):
        args    = task['args']
        if cmd in self._commandList:
            tasks.CMD[cmd](self._taskmanager, *args)
            
class SchedulerTaskHandler(BaseTaskHandler):
    
    def __init__(self, name):
        BaseTaskHandler.__init__(self, name)
        self._commandList = ['addScheduledTask', 'refreshServerStat','updateContractors','clean_commands','remove_old_links']
    
    