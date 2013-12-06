#
#
#
#
import http.server
import threading

class Listener(threading.Thread):
    
    def __init__(self, handler_class , router_instance):
        self._handler   = handler_class
        self._router    = router_instance
        self._httpd = None
        threading.Thread.__init__(self)
        
    def run(self):
        self.listen()
        
    def setEndpoint(self, server_address):
        self._endpoint  = server_address

    def listen(self):
        self._httpd = http.server.HTTPServer(self._endpoint, self._handler)
        self._httpd.request_router  = self._router
        self._httpd.serve_forever()
        
    def stop(self):
        if self._httpd is not None:
            self._httpd.shutdown()