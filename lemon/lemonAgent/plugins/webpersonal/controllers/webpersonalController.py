'''
Created on 20 янв. 2014 г.

@author: Andrean
'''
import os
import core
import shutil
import zipfile
import http
import socket
import subprocess

def copy_to(cmd):
    args    = cmd['args']
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
            raise Exception('Error while getting file')


def switch_service_path(cmd):
    args    = cmd['args']
    port    = args['port']
    hostname    = socket.gethostname()
    conn    = http.client.HTTPConnection(hostname,port)
    try:
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
            raise Exception("Changes not applied because {0}".format(str(res.reason)))
    finally:
        conn.close()


def switch_front_path(cmd):
    args    = cmd['args']
    iis_site    = args['iis_site']
    for record in args['items']:
        subprocess.check_call(['C:\\Windows\\System32\\inetsrv\\appcmd.exe','set','VDIR',iis_site+'/','/PhysicalPath:{0}'.format(os.path.normpath(record['path']))])

