#
#
#
#
import re
import types
import controllers.commandController as commandController


AGENT_INTERFACE_ROUTES  = [
    [  r'^/commands$', commandController.get_commands   ]
]

class Router(object):
    def __init__(self):
        self._routes    = []
        self._handler   = {}
    
    def apply_handler(self, request_handler):
        self._handler   = request_handler
        
    def dispatch(self, path):
        for rule in self._routes:
            if re.search(rule['pattern'], path):
                rule['action']( 
                    self.__make_request_ref(self._handler), 
                    self.__make_response_ref(self._handler) 
                )
            
    def add_route(self , url_pattern, action):
        self._routes.append( { 'pattern':url_pattern, 'action':action } )
            
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
        
                    