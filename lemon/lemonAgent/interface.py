'''
Created on 08.07.2013

@author: vau
'''

import time
import json
import lemon
import core
import queue
import http.client
import threading
import sys
import socket


ERROR_NOT_IDENTIFIED  = '0000001'
ERROR_NOT_AUTHORIZED  = '0000002'

TASK_SUCCESSFULLY_ADDED = '11'

RECONNECTION_INTERVAL      = 10
QUEUE_WAIT_INTERVAL         = 10

class HTTPClient(lemon.BaseAgentLemon):
    def __init__(self, _logger, _config, _info):
        self.agent_id = None
        self.serverEndpoint = ('localhost', 8080)
        self._reqQueue  = queue.Queue()
        self._safezone  = []
        lemon.BaseAgentLemon.__init__(self,_logger,_config, _info)
    
    def run(self):
        endpoint    = self._config.get('server',None)
        if endpoint:
            self.serverEndpoint = endpoint.split(':')
            self.serverEndpoint[1] = int(self.serverEndpoint[1])  
        self._setReady()
        while self._running:
            try:
                self._handle()
            except:
                self._logger.exception(sys.exc_info()[1])                
        self._logger.info('Shutdown client interface')
        
    def _handle(self):
        try:
            task = self._reqQueue.get(True,1)   # блокируем очередь и ждем элемент в течение не более 1 секунды
            connection  = task['conn']
            request     = task['req']
            callback    = task['cb']
            connection.request(*request)
            response    = connection.getresponse()
            callback(None, response)
        except queue.Empty:
            return
        except (ConnectionError, socket.timeout, http.client.HTTPException):        
            callback(sys.exc_info()[1],_reconnect=True)
        except:
            callback(sys.exc_info()[1])
            raise        
            
    def putRequest(self, connection, request, callback):
        while True:
            try:
                self._reqQueue.put( {'conn': connection, 'req': request, 'cb': callback}, True, QUEUE_WAIT_INTERVAL )
                return
            except queue.Full:
                self._logger.error('Queue is full')                
    
    def getHandler(self):
        return RequestHandler(self)
    
class   RequestHandler(object):
    def __init__(self, client):
        self.client     = client
        self.connection = http.client.HTTPConnection(self.client.serverEndpoint[0], self.client.serverEndpoint[1],timeout=5)
        self.mutex  = threading.Lock()
        self.connected = threading.Event()   
        self.connect()             
    
    def request(self, method, path, body=None, headers={}):
        if self.connected.wait(5) is False:     # максимальное время ожидания запроса. Если за это время не соединилось - послать запрос к черту
            return
        response    = {'result': None, 'error': None, 'ready': threading.Condition(self.mutex), 'reconnect': False}
        agentID       = core.getCoreInstance().getItem('agent')['__id']
        headers['Lemon-Agent-ID']   = agentID
        def callback( _error=None, _response=None, _reconnect = False ):
            response['result']   = _response 
            response['error']    = _error 
            response['reconnect']= _reconnect
            with response['ready']:           
                response['ready'].notify()
                
        self.client.putRequest( self.connection, [method, path, body, headers], callback )
        with response['ready']:
            response['ready'].wait()
        if response['error']:
            self.client._logger.error( response['error'] )                
            if response['reconnect']:
                self.connect()
            return                
        return response['result']
        
    def connect(self):
        t   = threading.Thread(None, self.__connect)
        t.setDaemon(True)
        t.start()
    
    def __connect(self):        
        self.connected.clear()
        self.connection.close()        
        while self.client.is_alive():
            try:
                self.connection.connect()
                self.connected.set()        
                self.client._logger.info('Connection to {0}:{1} sucessfully established'.format(str(self.client.serverEndpoint[0]), str(self.client.serverEndpoint[1])))
                return True
            except ConnectionError:
                self.client._logger.error('Connection to {0}:{1} failed. Reconnecting after {2} seconds'.format(self.client.serverEndpoint[0],
                                                                                                         str(self.client.serverEndpoint[1]), 
                                                                                                     str(RECONNECTION_INTERVAL)
                                                                                                     )
                                   )
                
                time.sleep(RECONNECTION_INTERVAL)
        return
    
    def send_json(self, obj, url, headers={}):
        body    = json.dumps(obj)
        headers['Content-Length']   = len(body)
        if 'Content-Type' not in headers.keys():
            headers['Content-Type'] = 'application/json'
        return self.request('POST', url, body, headers)
    
    def send_text(self, text, url, headers={}, encoding='utf-8'):
        body    = bytes(text,encoding)
        headers['Content-Length']   = len(body)
        if 'Content-Type' not in headers.keys():
            headers['Content-Type'] = 'text/plain' + ';charset={0}'.format(encoding)
        return self.request('POST', url, body, headers)
    
    def send_content(self, binary_data, url, headers={}):
        body    = binary_data
        headers['Content-Length']   = len(body)
        if 'Content-Type' not in headers.keys():
            headers['Content-Type'] = 'application/octet-stream'
        return self.request('POST', url, body, headers)
        
    def get_content(self, url, headers={}):
        return self.request('GET', url, "", headers)
    
    def get_file(self, url, headers={}):
        res = self.request('GET', url, "", headers)
        
        if res is None:
            return
        length      = res.headers.get('Content-Length',0)
        content_d  =  res.headers.get('Content-Disposition','')
        _type, _options = content_d.split(';')
        filename    = _options.split('filename=')[1].replace('"','')
        return { 'file': res, 'type': _type, 'filename': filename, 'length': int(length) }
    
    def close(self):
        self.connection.close()
        self.client._logger.info('Close connection to {0}:{1}'.format(self.client.serverEndpoint[0], str(self.client.serverEndpoint[1])))    
