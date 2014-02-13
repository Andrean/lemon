#
#
#
#
from urllib.parse import urlsplit
from urllib.parse import parse_qs
import re
import types
import sys
import json
import traceback
import core
import controllers.commandController as commandController
import controllers.baseController    as baseController
import controllers.dataController    as dataController
import controllers.webController     as webController
import controllers.fileController    as fileController

####
# LOADER FOR PLUGIN'S ROUTES
####
def loader(_filter, method):
    pm  = core.getCoreInstance().getInstance('PLUGIN_MANAGER')
    return pm.getRoutes(method, _filter)
#####################################################################################
#    Routes for routing agent's requests
#####################################################################################
AGENT_INTERFACE_ROUTES  = [
     [  'GET',  r'^/commands[?=%&\w]*$',  commandController.get_commands    ]
    ,[  'GET',  r'^/files[?=%,&_\-\w]*$',    fileController.get_files          ]
    ,[  '#LOAD',None, lambda: loader('agent','GET')   ] 
    ,[  'GET',  r'.*',           baseController.get_404                     ]
    ,[  'POST', r'^/commands/result$',  commandController.post_commands_result      ]    
    ,[  'POST', r'^/data/AgentState$',   dataController.post_agent_state    ]
    ,[  '#LOAD',None, lambda: loader('agent','POST')   ]
    ,[  'POST', r'.*',              baseController.get_404                  ]
    ,[  'PUT',  r'^/data$',         dataController.put_data                 ]
    ,[  '#LOAD',None, lambda: loader('agent','PUT')   ]
    ,[  'PUT',  r'.*',              baseController.get_404                  ]
    
]
#####################################################################################
#    Routes for routing request from WEB-Server as web-interface
#####################################################################################
WEB_INTERFACE_ROUTES = [
     [  'POST', r'^/upload$', webController.upload                          ]    
    ,[  'POST', r'^/agents$', webController.post_agents                     ]
    ,[  '#LOAD',None, lambda: loader('web','POST')   ]
    ,[  'POST', r'.*',              baseController.get_404                  ]
    ,[  'GET',  r'^/upload$', webController.test                            ]
    ,[  'GET',  r'^/agents$',   webController.get_agents                    ]
    ,[  'GET',  r'^/agents/update[?=%&_\-\+\w]*$',   webController.update_agents    ]
    ,[  'GET',  r'^/commands/status[?=%&_\-\+\w]*$',  webController.check_status    ]
    ,[  '#LOAD',None, lambda: loader('web','GET')   ]
    ,[  'GET',  r'.*',           baseController.get_404                     ]
    
]

class Router(object):
    def __init__(self, logger):
        self._routes    = []
        self._handler   = {}
        self._logger    = logger
        self.name       = "DEFAULT"
    
    def apply_handler(self, request_handler, method='GET'):
        self._handler   = request_handler
        self._method    = method
        
    def dispatch(self, path):
        for rule in self._routes:
            if rule['method'] == self._method and re.search(rule['pattern'], path):
                try:
                    rule['action']( 
                        self.__make_request_ref(self._handler, path), 
                        self.__make_response_ref(self._handler) 
                    )
                except:
                    self._logger.error('{0}\n{1}'.format(self.name, ''.join(traceback.format_exception(*(sys.exc_info())))))   
                    baseController.get_500( self.__make_request_ref(self._handler, path), self.__make_response_ref(self._handler) )
                return
            
    def add_route(self , method, url_pattern, action):
        if method == '#LOAD':
            self.__load(action())
            return
        self._routes.append( { 'pattern':url_pattern, 'action':action, 'method': method } )
          
    def load(self, routes):
        self._logger.debug('Loading routes')
        self.__load(routes)        
          
    def __load(self, routes): 
        for rule in routes:
            try:
                self.add_route(*rule)
            except Exception as e:
                self._logger.exception(e)
    
    def __make_request_ref(self, requestHandler, path):
        requestHandler.query  = parse_qs( (urlsplit(path)).query )       
        return requestHandler

    def __make_response_ref(self, requestHandler):
        def send_content(self, content, headers={}, code=200):
            self.send_response(code)
            self.send_header('Content-Type','text/plain;charset=utf-8')
            self.send_header('Content-Length',len(content))
            for header, value in headers.items():
                self.send_header(header, value)
            self.end_headers()
            self.wfile.write(bytes(content, 'utf-8')) 
        def send_json(self, content, headers={}, code=200):
            self.send_content( json.dumps(content), headers, code )   
        requestHandler.send_content = types.MethodType( send_content, requestHandler )
        requestHandler.send_json    = types.MethodType( send_json, requestHandler )        
        return requestHandler
    
            
class AgentInterfaceRouter(Router):
    def load(self):
        self.name   = 'AGENT LISTENER'
        super().load( AGENT_INTERFACE_ROUTES )
        
class WebInterfaceRouter(Router):
    def load(self):
        self.name   = 'WEB LISTENER'
        super().load( WEB_INTERFACE_ROUTES )
                    