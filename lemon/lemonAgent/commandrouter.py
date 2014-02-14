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
        [ '_.get_self_info',   baseController.get_self_info    ]
       ,[ '_.update_agent',    baseController.update_agent     ] 
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
        found   = False
        for rule in self.routes:
            if rule[0]  == command['cmd']:
                found = True
                try:
                    self.request_handler.sendCommandStatus(command['id'],status.pending)
                    rule[1](command)
                    self.request_handler.sendCommandStatus(command.get('id'), status.completed)
                except Exception as e:
                    self._logger.error('Command {0} completed with errors'.format(command.get('cmd')))
                    self._logger.exception(e);
                    self.request_handler.sendCommandStatus(command.get('id'), status.error, str(e))
                except:
                    self._logger.error('Command {0} completed with errors\n{1}'.format(command.get('cmd'),str(sys.exc_info()[1])))   
                    self.request_handler.sendCommandStatus(command.get('id'), status.error, str(sys.exc_info()[1]))
        if not found:
            self._logger.error('Command {0} not found\n{1}'.format(command.get('cmd'),'Command not found'))   
            self.request_handler.sendCommandStatus(command.get('id'), status.error, 'Command not found')

class CommandRouter(Router):
    def load(self):
        self.name   = 'COMMAND_ROUTER'
        pm  = core.getCoreInstance().pluginManager
        for route_list in pm.getCommands():
            COMMANDS.extend(route_list)
            self._logger.debug('Added commands: {0}'.format(str(route_list)))
        super().load( COMMANDS )