'''
Created on 13.06.2013

@author: vau
'''
from xmlrpcListener import xmlrpcListener
from xmlrpcListener import XMLRPCExitException
import httpListener
import httpHandler
import interface
import lemon
import uuid
import core
import router

class Server(lemon.BaseServerComponent):
    '''
    classdocs
    '''
    
    def __init__(self, _logger, _config, _info):
        lemon.BaseServerComponent.__init__(self, _logger, _config, _info)
        self._tmInstance    = None
        self.__instanceId   = uuid.uuid4();
        cfg                 = self._config
        self._xmlrpcListener    = xmlrpcListener((str(cfg['xmlrpc_address']), int(cfg['xmlrpc_port'])))
        aiRouter    = router.AgentInterfaceRouter()
        aiRouter.load()
        self._agentListener = httpListener.Listener(httpHandler.httpRequestHandler, aiRouter ) 
        self.cmdInterface   = None       

    def run(self):
        try:            
            coreInstance    = core.getCoreInstance()
            endpoint    = 'localhost:8080'
            if self._config.__contains__('agent_interface'):
                if self._config['agent_interface'].__contains__('listenerEndpoint'):
                    endpoint   = self._config['agent_interface']['listenerEndpoint']
            self._logger.info('http agent listener started')
            listenerAddr    = endpoint.split(':')
            self._agentListener.run(tuple([listenerAddr[0],int(listenerAddr[1])]))
            self._setReady()
            self._logger.info('http agent listener started')            
        except Exception as e:
            self._logger.exception(e)
    def shutdownListener(self):        
        self._agentListener.stop()
        self._logger.info('Server was successfully shutdown')
                
    def quit(self):
        super(Server, self).quit()
        self.shutdownListener()
        
    def _getId(self):
        return self.__instanceId;


    
        