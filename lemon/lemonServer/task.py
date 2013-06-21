'''
Created on 21.06.2013

@author: vau
'''

import threading 
import queue

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
        pass
    
    def _addTask(self, taskId, data):
        pass