'''
Created on 21.06.2013

@author: vau
'''

import threading 
import queue
import uuid
import time
import exception.lemonException as lemonException
import task_commands
import json
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
        self._storageManager    = cr.getInstance('STORAGE')
        self._setReady()
        self._logger.info("Task manager started")
        while(self._running):
            if self._checkForTasks():
                self._process()
            else:
                time.sleep(0.1)
        self._logger.info('Task Manager was successfully shutdown')
    
    def addTask(self, agentId, command, data):
        taskId  = str(uuid.uuid4())
        timestamp   = time.time()
        task    = [taskId,[agentId,command, timestamp, data]]
        self._logger.debug('add task %s' % taskId)
        self._addTask(task)
        
    def connectHandler(self, _handler):
        if _handler.getName() in self._handlerList.keys():
            raise lemonException.HandlerAlreadyInListException()
        else:
            self._handlerList[_handler.getName()] = _handler
            self._logger.debug('handler %s connected' % _handler.getName())
            
    def shutdown(self):
        self._logger.info('attempting to shutdown TaskManager')
        self._running   = False
        
    def _process(self):
        task = self._TaskQueue.get()
        taskId = task[0]
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
    
    @synchronized
    def _addTask(self, task):
        try:
            self._TaskQueue.put(task)
        except Exception as ex:
            print(ex)
        
        
class BaseTaskHandler(object):
    
    def __init__(self, _name):
        self._name  = _name
        self._commandList   = []
        
    def getName(self):
        return self._name
    
    def do(self, task):
        task_cmd = task[1][1]
        if task_cmd in self._commandList:
            try:
                self._dispatchMethod(task_cmd, task)
            except Exception as e:
                print( "Base task handler exception: %s" % str(e))
    
    def _dispatchMethod(self, cmd, task):
        pass
    
class StoreTaskHandler(BaseTaskHandler):
    
    def __init__(self, name, _agentStorageInstance):
        self._storage   = _agentStorageInstance
        BaseTaskHandler.__init__(self, name)
        self._commandList = [task_commands.CMD_STORE]
    
    def _dispatchMethod(self, cmd, task):
        agentId = task[1][0]
        timestamp   = task[1][2]
        data    = task[1][3]
        if cmd is task_commands.CMD_STORE:
            self._store(agentId, {'time':timestamp, 'data': data})
            
    def _store(self, agentId, data):
        itemId  = 'data_'+ agentId
        self._storage.appendToItem(itemId, json.dumps(data))
        
    