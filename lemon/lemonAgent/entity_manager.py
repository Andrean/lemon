'''
Created on 21.08.2013

@author: vau
'''

import lemon
import os
import core
import time
import collections
import json
import sys
import shutil
import zipfile
import socket
import http.client
import subprocess


CMD_STATUS  = collections.namedtuple('CMD_STATUS',['present','submit','pending','completed','error'])
status      = CMD_STATUS(
                present  = 0,
                submit    = 1,
                pending   = 2,
                completed = 3,
                error     = -1
            )

def commands_router(cmd_handler):
    t   = [
           ['get_self_info',    cmd_handler.get_self_info   ]
          ,['copy_to',          cmd_handler.copy_to         ]
          ,['switch_service_path',  cmd_handler.switch_service_path ]
          ,['switch_front_path',    cmd_handler.switch_front_path   ] 
    ]
    return t

class EntityManager(lemon.BaseAgentLemon):
   
    def __init__(self, _logger, _config, _info):
        lemon.BaseAgentLemon.__init__(self, _logger, _config, _info)
    
    def run(self):
        self.commandHandler = CommandHandler(self)
        self.commandHandler.load_router()
        self.commandHandler.schedule_self()
        self._setReady()
        while self._running:
            time.sleep(0.01)
        self.commandHandler.closeHandler()
        self._logger.info('Shutdown Entity Manager')
        
        
class CommandHandler(object):
    def __init__(self, manager):
        self.manager    = manager
        self.interface  = core.getCoreInstance().getInstance('INTERFACE')
        self.lemon_timestamp    = 0
        self.request_handler    = None
        self.router     = CommandRouter(self)
        
    def load_router(self):
        self.router.load(commands_router)
        
    def schedule_self(self):
        scheduler   = core.getCoreInstance().getInstance('SCHEDULER')
        if not scheduler.getScheduledTask('get_commands'):
            scheduler.add( 'get_commands', 'get_commands', start_time=None, interval=1 )
    
    def get_commands(self):
        print('{0}    - i am get commands'.format(time.asctime()))
        headers = {'Lemon-Agent-Timestamp': self.lemon_timestamp}
        if self.request_handler is None:
            self.request_handler  = self.interface.getHandler()        
        try:
            res = self.request_handler.get_content(  '/commands', headers  )
            if res is None:
                return
            print(res.status,res.reason)
            print(res.headers)
            try:
                if res.status == 200:
                    commands    = json.loads( str( res.read(), 'utf-8' ) )
                    # commands is a list of dicts such
                    # { 'cmd': string, 'args': [string], 'id': string }
                    #
                    for cmd in commands:
                        try:
                            self.router.dispatch(cmd, res.headers)
                            self.send_command_status(cmd['id'], status.completed)
                        except:
                            self.manager._logger.exception(sys.exc_info()[1])
                            self.send_command_status(cmd['id'], status.error)
                    self.lemon_timestamp    = res.headers.get('Lemon-Server-Timestamp','0') 
            finally:
                if not res.closed:
                    res.read()
        except:
            self.request_handler.close()
            self.request_handler    = None
            raise
    
    def send_command_status(self, cmd_id, status):
        self.manager._logger.info('Send command status to server.')
        headers = {'Lemon-Agent-Timestamp': self.lemon_timestamp}
        if self.request_handler is None:
            self.request_handler  = self.interface.getHandler()        
        try:
            res = self.request_handler.send_json([{'cmd_id': cmd_id, 'status': status}], '/commands/result', headers)
            if res is None:
                self.request_handler = None
                return
            try:
                if res.status == 200:
                    return True
                else:
                    return False
            finally:
                if not res.closed:
                    res.read()
        except:
            self.request_handler.close()
            raise
    
    def closeHandler(self):
        if self.request_handler:
            self.request_handler.close()
            
class CommandRouter():
    def __init__(self, handler):
        self.commands    = []
        self.handler    = handler
        
    def load(self, f):
        self.commands   = f(self)
        self.handler.manager._logger.debug('Commands was loaded')
        
    def dispatch(self, command, headers):
        for route in self.commands:
            if command.get('cmd', '') == route[0]:
                self.handler.send_command_status(command['id'],status.pending)
                route[1](command, headers)                
                return 
            
    def get_self_info(self, cmd, headers):
        print('exec get_self_info')
    
    def copy_to(self, cmd, headers):
        args    = cmd['args']
        cmd_id  = cmd['id']
        i   = core.getCoreInstance().getInstance('INTERFACE')
        rh  = i.getHandler()
        for record in args:
            link    = record['link']
            path    = os.path.normpath(record['path'])
            struct_file = rh.get_file('/files?file={0}'.format(link))
            if struct_file and struct_file['type'] == 'attachment':
                os.makedirs('files', exist_ok=True)                
                with open('files/'+struct_file['filename'],'wb') as f:
                    shutil.copyfileobj(struct_file['file'], f, struct_file['length'])
                    # теперь нужно распаковать архив, собрать список файлов и папок и оправить на сервер            
                zipfile.ZipFile('files/'+struct_file['filename']).extractall(path)
            else:
                raise Exception
            
    def switch_service_path(self, cmd, headers):
        args    = cmd['args']
        port    = args['port']
        hostname    = socket.gethostname()
        conn    = http.client.HTTPConnection(hostname,port)
        for record in args['items']:
            conn.request('GET','/GetServicePath?service={0}'.format(record['service']))
            res = conn.getresponse()
            if res.status != 200:
                conn.close()
                raise Exception()
            path    = str(res.read(),'utf-8')
            basefile    = os.path.basename(path)
            new_path    = os.path.join(os.path.normpath(record['path']),basefile)
            conn.request('GET','/ChangeServicePath?service={0}&fileName={1}'.format(record['service'],new_path))
            res = conn.getresponse()
            if res.status != 200:
                raise Exception()
            res.read()
        conn.request('GET','/ApplyChanges')
        res = conn.getresponse()
        if res.status != 200:
            raise Exception()
        conn.close()
            
    def switch_front_path(self, cmd, headers):
        args    = cmd['args']
        iis_site    = args['iis_site']
        for record in args['items']:
            subprocess.check_call(['C:\\Windows\\System32\\inetsrv\\appcmd.exe','set','VDIR',iis_site+'/','/PhysicalPath:{0}'.format(os.path.normpath(record['path']))])
        