'''
Created on 12.07.2013

@author: vau
'''

import time

class CommandInterface(object):
    '''
    classdocs
    '''


    def __init__(self, taskManager):
        '''
        Constructor
        '''
        self._taskManager   = taskManager
        self._commands  = {}
        self._current   = {}
        self._refresh   = time.time()
           
    def load(self):
        pass
    
    def getLastUpdateTime(self):
        return  self._refresh
    
    def getCurrentCommands(self):
        pass
    
    def getNewCommands(self):
        pass
    
    def getItem(self):
        pass
    