'''
Created on 13.06.2013

@author: vau
'''
import threading;

class Server(threading.Thread):
    '''
    classdocs
    '''
    __instanceId    = 0;
    def run(self):
        print("i am a new server instance with id: "+str(self._getId())+"\n");
                
    def _getId(self):
        return self.__instanceId;


    def __init__(self, _id):
        self.__instanceId = _id;
        threading.Thread.__init__(self);
        '''
        Constructor
        '''
        