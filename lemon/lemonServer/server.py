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
            self._logger.info('http agent listener started')
            self._agentListener.run(('localhost',8080))
            self._setReady()
            self._logger.info('http agent listener started')
        except Exception as e:
            self._logger.exception(e)    
        """
        try:
            _core   = core.getCoreInstance()
            self._tmInstance    = _core.getInstance('TASK_MANAGER')
            self.cmdInterface   = interface.CommandInterface(self._tmInstance)
            agentHandler        = interface.xmlrpcHandler(self._tmInstance, self.cmdInterface)
            self._xmlrpcListener.register_instance(agentHandler)
            self._setReady()
            self._logger.info('xmlrpc listener starting')
            self._xmlrpcListener.serve_forever()            
                        
        except XMLRPCExitException:
            print("xmlrpc server shutdown")
        self._logger.info('server instance with id {0} was stopped'.format(self._getId()))
        """
    def shutdownListener(self):        
        self._logger.info('attempting to shutdown agent xmlrpcListener')
        #self._xmlrpcListener.shutdown()
        #self._logger.info('agent xmlrpcListener is shutdown')
                
    def quit(self):
        super(Server, self).quit()
        self.shutdownListener()
        
    def _getId(self):
        return self.__instanceId;


    
        