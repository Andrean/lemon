'''
Created on 12.07.2013

@author: vau
'''

import time
import json
import uuid

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
        self._commandInterface.receive(agentId, json.loads(json_data))
        return TASK_SUCCESSFULLY_ADDED
    
    def refresh(self, agentId):
        result  = self._commandInterface.getLastUpdateTime()
        return result
    
    def get(self, agentId, key, *args):
        result = ""
        if key == 'new':
            result = self._commandInterface.getNewCommands(args[0], agentId)
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
        self._commands  = {'add_scheduled_task': {'__agents': 'all', 
                                                  '__add_timestamp': time.time(),\
                                                  '__type':'add_scheduled_task', 
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
    
    def receive(self, agentID, dict_data):
        agent_info  = {'agent': {'__id': agentID, 'received_id': dict_data['agent']['__id']}}
        agent_info['agent']['start_timestamp']  = time.time()
        agent_info['agent']['state']    = dict_data['agent']['state']
        agent_info['agent']['ip']       = dict_data['agent']['ip'] 
        self._taskManager.addTask('storeAgentData', agent_info)
        self._taskManager.addTask('storeData', dict_data)
        self._taskManager.addTask('storeCurrentData', dict_data)
            
    def getLastUpdateTime(self):
        return  self._refresh
    
    def getCurrentCommands(self,agentId=None):
        return self._commands
    
    def getNewCommands(self, lastread_timestamp = 0, agentId=None,):
        new = []
        for name, item in self._commands.items():
            if item['__add_timestamp'] > lastread_timestamp:
                new.append(name)  
        print('NEW COMMANDS: '+str(new))
        return new
    
    def getItem(self, agentId, key):
        try:
            return self._commands[key]
        except KeyError:
            return None

    def add(self, c_id, cmd_type, item):
        print('UPDATING COMMANDS: '+cmd_type)
        key = c_id
        self._refresh       = time.time()
        self._commands[key] = item
        self._commands[key]['__add_timestamp']   = self._refresh
        self._commands[key]['__type']   = cmd_type 
        print(self._commands)
        
    
    