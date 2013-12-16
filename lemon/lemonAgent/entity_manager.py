'''
Created on 21.08.2013

@author: vau
'''

import lemon
import core
import time
import collections
import json


CMD_STATUS  = collections.namedtuple('CMD_STATUS',['present','submit','pending','completed','error'])
status      = CMD_STATUS(
                present  = 0,
                submit    = 1,
                pending   = 2,
                completed = 3,
                error     = -1
            )

class EntityManager(lemon.BaseAgentLemon):
   
    def __init__(self, _logger, _config, _info):
        lemon.BaseAgentLemon.__init__(self, _logger, _config, _info)
    
    def run(self):
        self.commandHandler = CommandHandler(self)
        self.commandHandler.schedule_self()
        self._setReady()
        while self._running:
            time.sleep(0.01)
        self.commandHandler.closeHandler()
        self._logger.info('Shutdown Entity Manager')
        
        
class CommandHandler(object):
    def __init__(self, manager):
        self.manager    = manager
        self.interface  = core.getCoreInstance().getInstance('INTERFACE')
        self.lemon_timestamp    = 0
        self.request_handler    = None
        
    def schedule_self(self):
        scheduler   = core.getCoreInstance().getInstance('SCHEDULER')
        if not scheduler.getScheduledTask('get_commands'):
            scheduler.add( 'get_commands', 'get_commands', start_time=None, interval=1 )
    
    def get_commands(self):
        print('{0}    - i am get commands'.format(time.asctime()))
        headers = {'Lemon-Agent-Timestamp': self.lemon_timestamp}
        if self.request_handler is None:
            self.request_handler  = self.interface.getHandler()
        try:
            res = self.request_handler.get_content(  '/commands', headers  )
            if res is None:
                return
            print(res.status,res.reason)
            print(res.headers)
            try:
                if res.status == 200:
                    commands    = json.loads( str( res.read(), 'utf-8' ) )
                    self.lemon_timestamp    = res.headers.get('Lemon-Server-Timestamp','0') 
            finally:
                if not res.closed:
                    res.read()
        except:
            self.request_handler.close()
            raise
    
    def closeHandler(self):
        if self.request_handler:
            self.request_handler.close()