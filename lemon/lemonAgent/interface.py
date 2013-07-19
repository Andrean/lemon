'''
Created on 08.07.2013

@author: vau
'''

import time
import json
import xmlrpc.client
import lemon
import core
import queue


ERROR_NOT_IDENTIFIED  = '0000001'
ERROR_NOT_AUTHORIZED  = '0000002'

TASK_SUCCESSFULLY_ADDED = '11'


class XMLRPC_Client(lemon.BaseAgentLemon):
    '''
    classdocs
    '''


    def __init__(self, _logger, _config, _info):
        self._agentID   = None
        self._taskManager   = None
        self._server_addr   = _config['xmlrpc_server_addr']
        self._server_port   = _config['xmlrpc_server_port']
        self._last_refresh  = 0
        self._reqQueue  = queue.Queue()
        lemon.BaseAgentLemon.__init__(self,_logger,_config, _info)
        
    def run(self):
        self._taskManager   = core.getCoreInstance().getInstance('TASK_MANAGER')
        self._agentID       = core.getCoreInstance().getItem('agent')['__id']
        self._connection    = xmlrpc.client.ServerProxy('http://{0}:{1}'.format(self._server_addr, self._server_port))
        self._setReady()
        
        while(self._running):
            self._process()
            time.sleep(0.01)
            
    def _process(self):
        req = self._reqQueue.get()
        method  = req['method']
        args    = req['args']
        callback    = req['callback']
        if callback:
            result  = method(*args)
            callback(result)
        req['ready']    = True
    
    def _put(self, method, args=None, callback=None):
        request  = {'method': method, 'args': args, 'callback':callback, 'ready': False}
        self._reqQueue.put(request)
        return request
    
    def _formRequest(self, method, *args):
        result  = {'return': None}
        def callback(_result):
            result['return']   = _result
        p_task  = self._put(method, args, callback)
        print('BEGIN_' + str(p_task))
        while p_task['ready'] is not True:
            time.sleep(0.01)
        print('END_' + str(p_task))
        return result['return']
        
        
    def _reqREFRESH(self, agentID):
        return self._formRequest(self._connection.refresh, agentID)
        
    def _reqGET(self, agentID, key):
        return self._formRequest(self._connection.get, agentID, key)
    
    def _reqPOSTDATA(self, agentID, json_data):
        return self._formRequest(self._connection.postData, agentID, json_data)
        
    def post(self, data):
        code    = self._reqPOSTDATA(self._agentID,  json.dumps(data))
        if code is TASK_SUCCESSFULLY_ADDED:
            return True
        return False
    
    def get(self, key=None):
        try:
            if key is None:
                try:
                    result = self._reqREFRESH(self._agentID)
                    print(result)
                    if result - self._last_refresh > 0:
                        self._last_refresh  = result
                        self._taskManager.new_task('getNewData')
                except Exception as e:
                    self._logger.exception(e)                               
            else:
                result  = json.loads(self._reqGET(self._agentID, key))
                return result
        except Exception as e:
            self._logger.exception(e)
        