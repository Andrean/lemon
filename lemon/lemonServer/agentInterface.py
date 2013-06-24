'''
Created on 19.06.2013

@author: vau
'''

import common.IdGenerator
import time

SECONDS  = 1
MINUTES  = 60*SECONDS

NOT_IDENTIFIED  = 2

CMD_STORE       = 'store'

class AgentHandler(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self._sessionStorage = {}
        self._expireTime = 20 * MINUTES
    def startSession(self, _agentId):
        _sessionId = common.IdGenerator.GenerateSessionID()
        self._sessionStorage[_agentId] = {'id':_sessionId, 'expire': time.time() + self._expireTime}
        return _sessionId
    
    
    def postData(self, key, _dictData):
        agentId    = key[0]
        sessionId  = key[1]
        try:
            if self._sessionStorage[agentId] != sessionId:
                return NOT_IDENTIFIED  
        except KeyError:
            return
        
        self._TaskManager.addTask(agentId, CMD_STORE, _dictData)
                
        
    def _checkExpiredSessions(self):
        pass
            
    
    
    
    
    
         
    
    
