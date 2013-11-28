#
#
#
#
import http.server
import types


class httpRequestHandler(http.server.BaseHTTPRequestHandler):    
    def __init__(self, request, client_address, server):
        http.server.BaseHTTPRequestHandler.__init__(self, request, client_address, server)
                
    def do_GET(self):
        self._router    = self.server.request_router
        self._router.apply_handler(self)        
        """
        self.send_response(200)        
        self.send_header('Content-Type', 'text/plain;charset=utf-8')
        self.end_headers()
        self.wfile.write(bytes(self.path,'utf-8'))
        """
        self._router.dispatch(self.path)