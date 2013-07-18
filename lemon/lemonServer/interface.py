'''
Created on 12.07.2013

@author: vau
'''

import time
import task_commands

class CommandInterface(object):
    '''
    classdocs
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
    
    