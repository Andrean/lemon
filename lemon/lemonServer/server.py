'''
Created on 13.06.2013

@author: vau
'''
import threading;
from xmlrpcAgentListener import xmlrpcAgentListener
from xmlrpcAgentListener import XMLRPCExitException
from agentInterface import AgentHandler


class Server(threading.Thread):
    '''
    classdocs
    '''
    
    def __init__(self, _id, _cfg, _TaskManager):
        self._tmInstance    = _TaskManager
        self.__instanceId = _id;
        self._config    = _cfg
        cfg_ainterface  = self._config['AGENT_INTERFACE']
        self._xmlrpcListener = xmlrpcAgentListener((str(cfg_ainterface['xmlrpc_address']), int(cfg_ainterface['xmlrpc_port'])))
        threading.Thread.__init__(self);

    def run(self):
        try:
            agentHandler = AgentHandler(self._tmInstance)
            self._xmlrpcListener.register_instance(agentHandler)
            self._xmlrpcListener.serve_forever()            
        except XMLRPCExitException:
            print("xmlrpc server shutdown")
        print("i am a new server instance with id: "+str(self._getId())+"\n");
        
    
    def shutdownListener(self):
        self._xmlrpcListener.shutdown()
                
    def _getId(self):
        return self.__instanceId;


    
        