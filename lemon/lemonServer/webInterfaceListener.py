'''
Created on 13.06.2013

@author: vau
'''
import threading
import interfaceServer

class httpListener(interfaceServer.BaseInterfaceLinstener, threading.Thread):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        threading.Thread.__init__(self);
        pass
        