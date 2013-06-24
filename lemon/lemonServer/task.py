'''
Created on 21.06.2013

@author: vau
'''

import threading 
import queue
import uuid
import time

class TaskManager(threading.Thread):
    '''
    This manager manage task: read, write, add content and other
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self._TaskQueue = queue.Queue()
        self._lock  = threading.Lock()
        self._running   = False
        threading.Thread.__init__(self)
        
    def run(self):
        self._running   = True
        while(self._running):
            if self._checkForTasks():
                self._process()
            else:
                time.sleep(0.1)
    
    def addTask(self, agentId, command, data):
        taskId  = str(uuid.uuid4())
        task    = {taskId:[agentId,command, data]}
        self._addTask(task)
        
    def _process(self):
        pass
    
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
            