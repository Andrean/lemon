'''
Created on 21.08.2013

@author: vau
'''

import lemon
import core
import time
import json
import threading
import commandrouter

class EntityManager(lemon.BaseAgentLemon):
   
    def __init__(self, _logger, _config, _info):
        lemon.BaseAgentLemon.__init__(self, _logger, _config, _info)
    
    def run(self):
        self.commandHandler = CommandHandler(self)
        self.commandHandler.load_router()
        self.commandHandler.schedule_self()
        self._setReady()
        while self._running:
            time.sleep(0.01)
        self.commandHandler.closeHandler()
        self._logger.info('Shutdown Entity Manager')
        
        
class CommandHandler(object):
    def __init__(self, manager):
        self.lock       = threading.Lock()
        self.manager    = manager
        self.interface  = core.getCoreInstance().getInstance('INTERFACE')
        self.lemon_timestamp    = 0
        self.request_handler    = None
        self._logger    = self.manager._logger
        self.router     = commandrouter.CommandRouter(self)        
        
    def load_router(self):
        self.router.load()
        
    def schedule_self(self):
        scheduler   = core.getCoreInstance().getInstance('SCHEDULER')
        if not scheduler.getScheduledTask('get_commands'):
            scheduler.add( 'get_commands', 'get_commands', start_time=None, interval=1 )
    
    def get_commands(self):
        if self.lock.acquire(blocking=False) is False:
            return
        try:
            headers = {'Lemon-Agent-Timestamp': self.lemon_timestamp}
            if self.request_handler is None:
                self.request_handler  = self.interface.getHandler()        
            try:           
                res = self.request_handler.get_content( '/commands', headers  )
                if res is None:
                    return
                try:
                    if res.status == 200:
                        commands    = json.loads( str( res.read(), 'utf-8' ) )
                        # commands is a list of dicts such
                        # { 'cmd': string, 'args': [string], 'id': string }
                        #
                        self.lemon_timestamp    = res.headers.get('Lemon-Server-Timestamp','0')
                        for cmd in commands:
                            self.router.dispatch(cmd)                                             
                finally:
                    if not res.closed:
                        res.read()
            except:
                self.request_handler.close()
                self.request_handler    = None
                raise
        finally:
            self.lock.release()        
        
    def sendCommandStatus(self, cmd_id, status, msg=None):
        self.manager._logger.debug('Send command status to server.')
        headers = { 'Lemon-Agent-Timestamp': self.lemon_timestamp }
        if self.request_handler is None:
            self.request_handler  = self.interface.getHandler()        
        try:
            res = self.request_handler.send_json([{'cmd_id': cmd_id, 'status': status, 'msg':msg}], '/commands/result', headers)
            if res is None:
                self.request_handler = None
                return
            try:
                if res.status == 200:
                    return True                    
            finally:
                if not res.closed:
                    res.read()
            return False
        except:
            self.request_handler.close()
            raise
    
    def closeHandler(self):
        if self.request_handler:
            self.request_handler.close()            
