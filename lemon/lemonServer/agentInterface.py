'''
Created on 19.06.2013

@author: vau
'''

import common.IdGenerator
import time

SECONDS  = 1
MINUTES  = 60*SECONDS
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
        if _agentId not in self._sessionStorage:
            _sessionId = common.IdGenerator.GenerateSessionID()
            self._sessionStorage[_agentId] = {'id':_sessionId, 'expire': time.time() + self._expireTime}
            return _sessionId
        return self._sessionStorage[_agentId]['id']
    
    def _checkExpiredSessions(self):
        pass
            
    
    
    
    
    
         
    
    
