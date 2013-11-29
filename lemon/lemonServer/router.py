#
#
#
#
import re
import types
import controllers.commandController as commandController
import controllers.baseController as baseController


AGENT_INTERFACE_ROUTES  = [
     [  'GET', r'^/commands$',  commandController.get_commands  ]
    ,[  'GET', r'.*',           baseController.get_404          ]
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
                        self.__make_request_ref(self._handler), 
                        self.__make_response_ref(self._handler) 
                    )
                except:                    
                    baseController.get_500( self.__make_request_ref(self._handler), self.__make_response_ref(self._handler) )
                return
            
    def add_route(self , method, url_pattern, action):
        self._routes.append( { 'pattern':url_pattern, 'action':action, 'method': method } )
            
    def load(self, routes):
        for rule in routes:
            self.add_route(*rule)
    
    def __make_request_ref(self, requestHandler):
        return requestHandler

    def __make_response_ref(self, requestHandler):
        def send_content(self, content):
            self.wfile.write(bytes(content, 'utf-8'))    
        requestHandler.send_content = types.MethodType( send_content, requestHandler )
        return requestHandler
    
            
class AgentInterfaceRouter(Router):
    def load(self):
        super().load( AGENT_INTERFACE_ROUTES )
        
                    