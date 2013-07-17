'''
Created on 08.07.2013

@author: vau
'''

import time
import json
import xmlrpc.client
import lemon
import core


ERROR_NOT_IDENTIFIED  = '0000001'
ERROR_NOT_AUTHORIZED  = '0000002'

TASK_SUCCESSFULLY_ADDED = '11'



class XMLRPC_Client(lemon.BaseAgentLemon):
    '''
    classdocs
    '''


    def __init__(self, _logger, _config, _info):
        self._logger    = _logger
        self._config    = _config
        self._running   = False
        self._agentID   = None
        self._taskManager   = None
        self._server_addr   = _config['xmlrpc_server_addr']
        self._server_port   = _config['xmlrpc_server_port']
        self._last_refresh  = 0
        lemon.BaseAgentLemon.__init__(self,_logger,_config, _info)
        
    def run(self):
        self._taskManager   = core.getCoreInstance().getInstance('TASK_MANAGER')
        self._agentID       = core.getCoreInstance().getItem('agent')['__id']
        self._connection    = xmlrpc.client.ServerProxy('http://{0}:{1}'.format(self._server_addr, self._server_port))
        self._setReady()
        
        while(self._running):
            time.sleep(0.01)
            
    def post(self, data):
        code    = self._connection.postData(self._agentID, json.dumps(data))
        if code is TASK_SUCCESSFULLY_ADDED:
            return True
        return False
    
    def get(self, key=None):
        try:
            if key is None:
                try:
                    result  = self._connection.refresh(self._agentID)
                    print(result)
                    if result - self._last_refresh > 0:
                        self._last_refresh  = result
                        self._taskManager.new_task('getNewData')
                except Exception as e:
                    self._logger.exception(e)                               
            else:
                result  = json.loads(self._connection.get(self._agentID, key))
                return result
        except Exception as e:
            self._logger.exception(e)
        