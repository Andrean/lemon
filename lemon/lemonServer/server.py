'''
Created on 13.06.2013

@author: vau
'''
import httpListener
import httpHandler
import lemon
import uuid
import router

class Server(lemon.BaseServerComponent):
    
    def __init__(self, _logger, _config, _info):
        lemon.BaseServerComponent.__init__(self, _logger, _config, _info)
        self._tmInstance    = None
        self.__instanceId   = uuid.uuid4();
        aiRouter    = router.AgentInterfaceRouter()
        aiRouter.load()
        webRouter   = router.WebInterfaceRouter()
        webRouter.load()
        self._agentListener = httpListener.Listener(httpHandler.httpRequestHandler, aiRouter )
        self._webListener   = httpListener.Listener(httpHandler.httpRequestHandler, webRouter) 
        self.cmdInterface   = None       

    def run(self):
        try:            
            ai_endpoint = self._config.get('agent_interface', {'listenerEndpoint': 'localhost:8080'}).get('listenerEndpoint','localhost:8080')
            web_endpoint = self._config.get('web_interface', {'listenerEndpoint': 'localhost:10003'}).get('listenerEndpoint','localhost:10003')            
            ai_listenerAddr    = ai_endpoint.split(':')
            self._agentListener.setEndpoint(tuple([ai_listenerAddr[0],int(ai_listenerAddr[1])]))
            web_listenerAddr    = web_endpoint.split(':')
            self._webListener.setEndpoint(tuple([web_listenerAddr[0],int(web_listenerAddr[1])]))            
            self._agentListener.start()
            self._logger.info('http agent listener started')          
            self._webListener.start()
            self._logger.info('http WEB listener started')          
            self._setReady()              
        except Exception as e:
            self._logger.exception(e)
            raise
        
    def shutdownListener(self):        
        self._agentListener.stop()
        self._webListener.stop()
        self._logger.info('Server was successfully shutdown')
                
    def quit(self):
        super(Server, self).quit()
        self.shutdownListener()
        
    def _getId(self):
        return self.__instanceId;


    
        