'''
Created on 19.06.2013

@author: vau
'''

import common.timer
import time
import task_commands

SECONDS  = 1
MINUTES  = 60*SECONDS



ERROR_NOT_IDENTIFIED  = '0000001'
ERROR_NOT_AUTHORIZED  = '0000002'

TASK_SUCCESSFULLY_ADDED = '11'

        
class AgentHandler(object):
    '''
    classdocs
    '''


    def __init__(self, _taskmanager, interface):
        '''
        Constructor
        '''
        self._TaskManager   = _taskmanager
        self._commandInterface  = interface
        
        
    
    def postData(self, agentId, _dictData):
        self._TaskManager.addTask(agentId, task_commands.CMD_STORE, _dictData)
        return TASK_SUCCESSFULLY_ADDED
    
    def refresh(self, agentId):
        result  = self._commandInterface.getLastUpdateTime()
        return result
    
    def get(self, agentId, key):
        if key == 'new':
            print('Getting key "new" from agent {0}'.format(agentId))
    
    def getUpdate(self, agentId, _dictData):
        pass
    
    def getConfig(self, agentId, _dictData):
        pass
                
        
   
            
           
    
    
    
    
    
         
    
    
