'''
Created on 13.06.2013

@author: vau
'''
import server
import webInterfaceListener

if __name__ == '__main__':
    agentServerInstance      = server.Server(20);
    httpInterfaceInstance    = webInterfaceListener.httpListener();
    
    agentServerInstance.start();
    httpInterfaceInstance.start();