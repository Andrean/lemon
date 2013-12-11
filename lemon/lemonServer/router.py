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
import controllers.commandController as commandController
import controllers.baseController    as baseController
import controllers.dataController    as dataController
import controllers.webController     as webController
import controllers.fileController    as fileController

#####################################################################################
#    Routes for routing agent's requests
#####################################################################################
AGENT_INTERFACE_ROUTES  = [
     [  'GET',  r'^/commands[?=%&\w]*$',  commandController.get_commands    ]
    ,[  'GET',  r'^/files[?=%,&_\-\w]*$',    fileController.get_files          ] 
    ,[  'GET',  r'.*',           baseController.get_404                     ]
    ,[  'POST', r'^/commands/result$',  commandController.post_commands_result      ]    
    ,[  'POST', r'^/data/AgentState$',   dataController.post_agent_state    ]
    ,[  'POST', r'.*',              baseController.get_404                  ]
    ,[  'PUT',  r'^/data$',         dataController.put_data                 ]
    ,[  'PUT',  r'.*',              baseController.get_404                  ]
    
]
#####################################################################################
#    Routes for routing request from WEB-Server as web-interface
#####################################################################################
WEB_INTERFACE_ROUTES = [
     [  'POST', r'^/upload$', webController.upload                          ]
    ,[  'POST', r'^/update/distr$', webController.post_distr                ]
    ,[  'POST', r'^/update/copy_to_agents$', webController.copy_services_to_agents   ]
    ,[  'POST', r'^/agents$', webController.post_agents                     ]
    ,[  'POST', r'.*',              baseController.get_404                  ]
    ,[  'GET',  r'^/upload$', webController.test                            ]
    ,[  'GET',  r'^/agents$',   webController.get_agents                    ]
    ,[  'GET',  r'.*',           baseController.get_404                     ]
    
]

class Router(object):
    def __init__(self):
        self._routes    = []
        self._handler   = {}
    
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
                    traceback.print_exception(sys.exc_info()[0],sys.exc_info()[1],sys.exc_info()[2])                   
                    baseController.get_500( self.__make_request_ref(self._handler, path), self.__make_response_ref(self._handler) )
                return
            
    def add_route(self , method, url_pattern, action):
        self._routes.append( { 'pattern':url_pattern, 'action':action, 'method': method } )
            
    def load(self, routes):
        for rule in routes:
            self.add_route(*rule)
    
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
        super().load( AGENT_INTERFACE_ROUTES )
        
class WebInterfaceRouter(Router):
    def load(self):
        super().load( WEB_INTERFACE_ROUTES )
                    