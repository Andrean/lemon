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
    __instanceId    = 0;
    def run(self):
        try:
            self._xmlrpcListener.register_instance(AgentHandler())
            self._xmlrpcListener.serve_forever()            
        except XMLRPCExitException:
            print("xmlrpc server shutdown")
        print("i am a new server instance with id: "+str(self._getId())+"\n");
        
    
    def shutdownListener(self):
        self._xmlrpcListener.shutdown()
                
    def _getId(self):
        return self.__instanceId;


    def __init__(self, _id):
        self.__instanceId = _id;
        self._xmlrpcListener = xmlrpcAgentListener(('test-note.kontur', 8000))
        threading.Thread.__init__(self);
        '''
        Constructor
        '''
        