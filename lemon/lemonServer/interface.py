'''
Created on 12.07.2013

@author: vau
'''

import core
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
        self._commandInterface.receive(agentId, json.loads(json_data))
        return TASK_SUCCESSFULLY_ADDED
    
    def refresh(self, agentId):
        result  = self._commandInterface.getRevision()        
        #result  = self._commandInterface.getLastUpdateTime()
        return result
    
    def get(self, agentId, key, *args):
        result = ""
        if key == 'cfg':
            result  = self._commandInterface.getConfig(agentId)
            return json.dumps(result)
        if key == 'cmd':
            result  = self._commandInterface.getCMD(agentId)            
            return json.dumps(result)
        if key == 'file':
            result = self._commandInterface.getFile(agentId, args[0])
            return json.dumps(result)
                
        if key == 'new':
            result = self._commandInterface.getNewCommands(args[0], agentId)
        elif key == 'all':
            result = self._commandInterface.getCurrentCommands(agentId)
        else:
            result =  self._commandInterface.getItem(agentId, key)
        return json.dumps(result)    
    

class CommandInterface(object):
    '''
    high interface for server 
    '''


    def __init__(self, taskManager):
        '''
        Constructor
        '''
        self._taskManager   = taskManager
        self._commands  = {}
        self._revision  = 0
        self._entityManager = core.getCoreInstance().getInstance('ENTITY_MANAGER')       
        
        '''
        config    = {
            'item-id':     {
                            '__type': type,
                            '__tags': [tags],
                            '__added': time,
                            '__revision': autoincrement number   
                            'content' : {item-content}
                            }        
                    }
        '''
        '''
        self._commands  = {'identifikator': {     '__agents': 'all', 
                                                  '__add_timestamp': time.time(),\
                                                  '__type':'add_scheduled_task', 
                                                  'content': {
                                                               'func': 'testPrint',
                                                               'name': 'testPrint',
                                                               'interval': 5*60,
                                                               'start_time': None,
                                                               'kwargs': {'los': 'test', 't': True}
                                                              }}}
        '''
        self._current   = {}
        self._refresh   = time.time()
           
    def load(self):
        pass
    
    def receive(self, agentID, dict_data):
        self._taskManager.addTask('storeAgentData', dict_data)
        self._taskManager.addTask('storeCurrentData', dict_data)
        self._taskManager.addTask('storeData', dict_data)
        
    def getRevision(self):
        return self._entityManager.configManager.getRevision()
            
    def getLastUpdateTime(self):
        return  self._refresh
    
    def getConfig(self, agentId):         
        return {'v':self.getRevision(), 'cfg': [x for x in self._entityManager.getConfig(agentId)]}
        
    def getCMD(self, agentId):
        return {'cmd': self._entityManager.getCommands(agentId)}
    
    def getFile(self, agentId, file_id):
        return {'file': self._entityManager.getFile(agentId, file_id)}
    
    def getCurrentCommands(self,agentId=None):
        return self._commands
    
    def getNewCommands(self, lastread_timestamp = 0, agentId=None,):
        new = []
        for name, item in self._commands.items():
            if item['__add_timestamp'] > lastread_timestamp:
                if len(new) < 1:
                    new.append(name)
                for i,v in enumerate(new):
                    if self._commands[v]['__add_timestamp'] > item['__add_timestamp']:
                        new.insert(i, name)
                        break
                          
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
        remove_list = []
        for k, v in self._commands.items():
            if v['content']['name'] == item['content']['name']:
                remove_list.append(k)
        for i in remove_list:
            self._commands.pop(i)
        self._refresh       = time.time()
        self._commands[key] = item
        self._commands[key]['__add_timestamp']   = self._refresh
        self._commands[key]['__type']   = cmd_type        
        


        