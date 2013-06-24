'''
Created on 21.06.2013

@author: vau
'''

import threading 
import queue
import uuid

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
        threading.Thread.__init__(self)
        
    def run(self):
        pass
    
    def addTask(self, agentId, data):
        taskId  = str(uuid.uuid4())
        task    = {taskId:[agentId,data]}
        self._addTask(task)
        
    
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
            