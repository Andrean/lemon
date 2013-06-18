'''
Created on 14.06.2013

@author: vau
'''

import sys
import os
import common.IdGenerator
import threading
import time


class Storage(threading.Thread):
    '''
    Class using different files for every item
    '''
    def __init__(self, preinitFile, logger, cfg):
        '''
        Constructor
        '''
        self._lock  = threading.Lock()
        self._encoding  = 'utf-8'
        self._logger    = logger
        self._config    = cfg
        try:
            self._path  = self._config['data_path']
        except KeyError as k:
            self._logger.error("config error. Cannot create storage {0} : {1}".format(self._storageID, str(k)))
            return
        
        self._storageID = self._read(self._path + preinitFile) or ''
        
        if  self._storageID is '':                                        
            self._storageID = common.IdGenerator.GenerateNewUniqueID();
            logger.info("storage create new ID")
            self._write(self._path + preinitFile, self._storageID)
        else:
            self._storageID = str(self._storageID, self._encoding)
        
        threading.Thread.__init__(self)
        self._logger.info("storage created with Id " + self._storageID)
        
                 
    def run(self):
        self._running = True
        self._logger.info("storage {0} started".format(self._storageID))
        if not os.path.exists(self._config['data_path']):
            os.makedirs(self._config['data_path'])
        while(self._running):
            time.sleep(0.1)
        print(self._storageID)
        
    # return byte content from file
    def readItem(self, item_id):
        fileName = self._getFilename(item_id);
        return self._read(fileName);
    
    # transform content to byte sequence and write it into file
    def writeItem(self, item_id, content):
        fileName = self._getFilename(item_id);
        return self._write(fileName, content);
    
    def _read(self, file):
        try:
            self._dolock()
            f = open(file, 'rb');
            content = f.read()
            f.close()
            return content
        except IOError:
            self._logger.info("{0} is not exists. Creating new file".format(str(file)));
        except Exception as ex:
            tb  = sys.exc_info()[2]
            self._logger.error(ex.with_traceback(tb))
        finally:
            self._unlock()
                      
    def _write(self, file, content):
        try:
            self._dolock()
            f = open(file, 'wb')
            f.write(bytes(content, self._encoding))
            return True
        except Exception as ex:
            tb = sys.exc_info()[2]
            self._logger.error(ex.with_traceback(tb))
        finally:
            f.close()
            self._unlock()
            
        
            
    def _getFilename(self, item_id):
        return self._path + '/' + self._storageID + str(item_id);
        
    def _dolock(self):
        self._lock.acquire()
        
    def _unlock(self):
        self._lock.release()
        
    def quit(self):
        self._running = False