import http.server
class Listener(object):


    def __init__(self, handler_class , router_instance):
        self._handler   = handler_class
        self._router    = router_instance
        self._httpd = None
        
    def run(self, server_address):
        self._httpd = http.server.HTTPServer(server_address, self._handler)
        self._httpd.request_router  = self._router
        self._httpd.serve_forever()
        