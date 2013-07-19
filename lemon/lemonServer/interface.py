'''
Created on 12.07.2013

@author: vau
'''

import time
import json

SECONDS  = 1
MINUTES  = 60*SECONDS

TASK_SUCCESSFULLY_ADDED = '11'


class xmlrpcHandler(object):
    '''
    low interface for agents
    '''
    def __init__(self, _taskmanager, interface):
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

class CommandInterface(object):
    '''
    high interface for server 
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
    
    def post(self, agentID, dict_data):
        agent_info  = {'agent': {'__id': agentID, 'received_id': dict_data['agent']['__id']}}
        agent_info['agent']['start_timestamp']  = time.time()
        agent_info['agent']['state']    = dict_data['agent']['state']
        agent_info['agent']['ip']       = dict_data['agent']['ip'] 
        print(agent_info)
        # TODO: store in database
    
    def getLastUpdateTime(self):
        return  self._refresh
    
    def getCurrentCommands(self, agentId = None):
        return self._commands
    
    def getNewCommands(self, agentId = None):
        return self._new
    
    def getItem(self, agentId, key):
        try:
            return self._commands[key]
        except KeyError:
            return None
    
    def updateCommands(self, commandsDict):
        pass
    
    