'''
Created on 19.06.2013

@author: vau
'''

import common.timer
import time
import json
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
    
    def postData(self, agentId, json_data):
        self._commandInterface.post(agentId, json.loads(json_data))
        return TASK_SUCCESSFULLY_ADDED
    
    def refresh(self, agentId):
        result  = self._commandInterface.getLastUpdateTime()
        return result
    
    def get(self, agentId, key):
        result = ""
        if key == 'new':
            result = self._commandInterface.getNewCommands(agentId)
        elif key == 'all':
            result = self._commandInterface.getCurrentCommands(agentId)
        else:
            result =  self._commandInterface.getItem(agentId, key)
        return json.dumps(result)
    
    def getUpdate(self, agentId, _dictData):
        pass
    
    def getConfig(self, agentId, _dictData):
        pass
                
        
   
            
           
    
    
    
    
    
         
    
    
