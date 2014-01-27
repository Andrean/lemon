'''
Created on 20 янв. 2014 г.

@author: Andrean
'''
import sys
import core
import collections
from controllers import baseController

CMD_STATUS  = collections.namedtuple('CMD_STATUS',['present','submit','pending','completed','error'])
status      = CMD_STATUS(
                present   = 0,
                submit    = 1,
                pending   = 2,
                completed = 3,
                error     = -1
            )
##############################################################################
#    Commands routing table
##############################################################################
COMMANDS    = [
        [ 'get_self_info',   baseController.get_self_info    ]
    ]
##############################################################################


##############################################################################
class   Router(object):
    def __init__(self, _request_handler):
        self.routes = [];
        self.name   = 'DEFAULT_ROUTER'
        self.request_handler = _request_handler
        self._logger    = _request_handler._logger
    
    def load(self, routes):
        self.routes[:]  = routes;
        
    def dispatch(self, command):
        for rule in self.routes:
            if rule[0]  == command['cmd']:
                try:
                    self.request_handler.sendCommandStatus(command['id'],status.pending)
                    rule[1](command)
                    self.request_handler.sendCommandStatus(command.get('id'), status.completed)
                except:
                    self._logger.error('Command {0} completed with errors\n{1}'.format(command.get('cmd'),str(sys.exc_info()[1])))   
                    self.request_handler.sendCommandStatus(command.get('id'), status.error, str(sys.exc_info()[1]))

class CommandRouter(Router):
    def load(self):
        self.name   = 'COMMAND_ROUTER'
        pm  = core.getCoreInstance().pluginManager
        for route_list in pm.getCommands():
            COMMANDS.extend(route_list)
        super().load( COMMANDS )