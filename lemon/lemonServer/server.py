'''
Created on 13.06.2013

@author: vau
'''
from xmlrpcListener import xmlrpcListener
from xmlrpcListener import XMLRPCExitException
import interface
import lemon
import uuid
import core

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

    def run(self):
        try:
            _core   = core.getCoreInstance()
            self._tmInstance    = _core.getInstance('TASK_MANAGER')
            cmdInterface    = interface.CommandInterface(self._tmInstance)
            agentHandler = interface.xmlrpcHandler(self._tmInstance, cmdInterface)
            self._xmlrpcListener.register_instance(agentHandler)
            self._setReady()
            self._logger.info('xmlrpc listener starting')
            print("i am a new server instance with id: "+str(self._getId())+"\n");
            self._xmlrpcListener.serve_forever()
                        
        except XMLRPCExitException:
            print("xmlrpc server shutdown")
        self._logger.info('server instance with id {0} was stopped'.format(self._getId()))
        
        
    
    def shutdownListener(self):
        self._logger.info('attempting to shutdown agent xmlrpcListener')
        self._xmlrpcListener.shutdown()
        self._logger.info('agent xmlrpcListener is shutdown')
                
    def _getId(self):
        return self.__instanceId;


    
        