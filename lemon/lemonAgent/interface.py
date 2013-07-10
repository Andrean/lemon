'''
Created on 08.07.2013

@author: vau
'''

import threading
import time
import xmlrpc.client


ERROR_NOT_IDENTIFIED  = '0000001'
ERROR_NOT_AUTHORIZED  = '0000002'

TASK_SUCCESSFULLY_ADDED = '11'


class XMLRPC_Client(threading.Thread):
    '''
    classdocs
    '''


    def __init__(self, _logger, _config, _agentID):
        self._logger    = _logger
        self._config    = _config
        self._running   = False
        self._agentID   = _agentID
        self._server_addr   = _config['xmlrpc_server_addr']
        self._server_port   = _config['xmlrpc_server_port']
        threading.Thread.__init__(self)
        
    def run(self):
        conn    = self._connection    = xmlrpc.client.ServerProxy('http://{0}:{1}'.format(self._server_addr. self._server_port))
        self._running = True
        
        while(self._running):
            time.sleep(0.01)
            
        
    def quit(self):
        self._running = False
        
    def set_session(self):
        self._sessionID = self._connection.startSession(self._agentID)
        
    def post(self, data):
        code    = self._connection.postData(self._agentID, self._sessionID, data)
        if code is ERROR_NOT_AUTHORIZED:
            self.set_session()
            code = self._connection.postData(self._agentID, self._sessionID, data)
        if code is TASK_SUCCESSFULLY_ADDED:
            return True
        return False
    
    def get(self, key):
        pass
        
    def isReady(self):
        if self._running:
            return True
        return False