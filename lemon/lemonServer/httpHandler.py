#
#
#
#
import http.server

class httpRequestHandler(http.server.BaseHTTPRequestHandler):    
    def __init__(self, request, client_address, server):        
        self.protocol_version = 'HTTP/1.1'
        http.server.BaseHTTPRequestHandler.__init__(self, request, client_address, server)        
                
    def do_GET(self):
        router    = self.server.request_router
        router.apply_handler(self, 'GET')
        router.dispatch(self.path)
        
    def do_POST(self):
        router    = self.server.request_router
        router.apply_handler(self, 'POST')
        router.dispatch(self.path)