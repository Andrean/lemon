'''
Created on 12.07.2013

@author: vau
'''

import time
import json

class CommandInterface(object):
    '''
    classdocs
    '''


    def __init__(self, taskManager):
        '''
        Constructor
        '''
        self._taskManager   = taskManager
        self._commands  = {'add_scheduled_task': {'agents': 'all', 
                                                  'timestamp': time.time(), 
                                                  'content': {
                                                               'func': 'testPrint',
                                                               'name': 'testPrint',
                                                               'interval': 5*60,
                                                               'start_time': None,
                                                               'kwargs': {'los': 'test', 't': True}
                                                              }}}
        self._new       = ['add_scheduled_task']
        self._current   = {}
        self._refresh   = time.time()
           
    def load(self):
        pass
    
    def getLastUpdateTime(self):
        return  self._refresh
    
    def getCurrentCommands(self):
        return self._commands
    
    def getNewCommands(self):
        return self._new
    
    def getItem(self, key):
        try:
            return json.dumps(self._commands[key])
        except KeyError:
            return None
    
    def updateCommands(self, commandsDict):
        pass
    
    