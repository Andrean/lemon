'''
Created on 21.06.2013

@author: vau
'''

import threading 
import queue
import uuid
import time
import exception.lemonException as lemonException

class TaskManager(threading.Thread):
    '''
    This manager manage task: read, write, add content and other
    '''


    def __init__(self, logger, cfg):
        '''
        Constructor
        '''
        self._TaskQueue = queue.Queue()
        self._lock  = threading.Lock()
        self._logger    = logger
        self._config    = cfg
        self._running   = False
        self._handlerList   = {}
        threading.Thread.__init__(self)
        
    def run(self):
        self._running   = True
        self._logger.info("Task manager started")
        while(self._running):
            if self._checkForTasks():
                self._process()
            else:
                time.sleep(0.1)
    
    def addTask(self, agentId, command, data):
        taskId  = str(uuid.uuid4())
        task    = {taskId:[agentId,command, data]}
        self._addTask(task)
        
    def connectHandler(self, _handler):
        if _handler.getName() in self._handlerList.keys():
            raise lemonException.HandlerAlreadyInListException()
        else:
            self._handlerList[_handler.getName()] = _handler
        
    def _process(self):
        task = self._TaskQueue.get()
        taskId = task.keys()[0]
        try:
            self._logger.debug("Task {0} is processed".format(taskId))
            for taskHandler in self._handlerList.values():
                taskHandler.do(task)
            self._logger.debug("Task {0} was processed without errors".format(taskId))
        except Exception as e:
            self._logger.error("Task {0} was processed with error: {1}".format(taskId, str(e)))
            
    def _checkForTasks(self):
        if self._TaskQueue.empty():
            return False
        return True
    
    def _addTask(self, task):
        try:
            self._dolock()
            self._TaskQueue.put(task)
            self._unlock()
        except Exception as ex:
            print(ex)
    
    def _dolock(self):
        self._lock.acquire()
        
    def _unlock(self):
        self._lock.release()
            