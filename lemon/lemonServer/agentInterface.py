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


    def __init__(self, _taskmanager):
        '''
        Constructor
        '''
        self._TaskManager   = _taskmanager
        self._sessionStorage = {}
        self._expireTime    = 20 * MINUTES
        self._interval      = 5 * SECONDS 
        expiredSessionsTimer   = common.timer.RepeatedTimer(self._interval, self._checkExpiredSessions)
        expiredSessionsTimer.start()
        
    
    def postData(self, agentId, sessionId, _dictData):
        self._TaskManager.addTask(agentId, task_commands.CMD_STORE, _dictData)
        return TASK_SUCCESSFULLY_ADDED
    
    def refresh(self, agentId, sessionId):
        pass
    
    def get(self, agentId, sessionId):
        pass
    
    def getUpdate(self, agentId, sessionId, _dictData):
        pass
    
    def getConfig(self, agentId, sessionId, _dictData):
        pass
                
        
    def _checkExpiredSessions(self):
        removeList = [k for k, v in self._sessionStorage.items() if v['expire'] < time.time()]
        for k in removeList:
            self._sessionStorage.pop(k)
            
           
    
    
    
    
    
         
    
    
