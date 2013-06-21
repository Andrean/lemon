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
        
    def run(self):
        pass
    
    def addTask(self, agentId, data):
        taskId  = str(uuid.uuid4())
        task    = {taskId:[agentId,data]}
        self._addTask(task)
        
    
    def _addTask(self, task):
        try:
            self._TaskQueue.put(task)
        except Exception as ex:
            print(ex)
            
            