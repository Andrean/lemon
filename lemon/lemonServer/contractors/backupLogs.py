#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    contractor: backupLogs
    backuping logs with archiving and sending them to backup server
    
    Author:    Andrean
'''

import os
import sys
import socket
import stat
import time
import shutil
import gzip
import tarfile

VERSION = '0.0.1'

config  = {
            'savePeriod': 7,    # за сколько дней от текущей даты архивировать логи
            'logStoragePath': r"\\localhost\e$\bkp\logs\\"
             
           }
def backupLogs( path, config ):
    hostName    = socket.gethostname()
    backupPath  = path + '\\..\\.lemon_backup_tmp'
    if os.path.exists(backupPath) is False:
        os.makedirs(backupPath)
    moveLogs( path, backupPath, config['savePeriod'] )
    archive_name    = getTimeLabel()
    archive_list    = {}    
    for srv in os.listdir(backupPath):
        f_entry  = os.path.join(backupPath, srv)
        if os.path.isdir(f_entry):
            servicePath = f_entry
            for sub_entry in os.listdir(servicePath):
                tar_name    = archive_name + "_" + sub_entry
                subservicePath  = os.path.join(servicePath, sub_entry)
                if os.path.isdir(subservicePath):
                    for file in os.listdir(subservicePath):
                        pass
                        tar(os.path.join(f_entry, tar_name), os.path.join(subservicePath, file))
                else:
                    pass
                    tar(os.path.join(f_entry, archive_name), os.path.join(servicePath, sub_entry))
            archive_list[srv]   = [] 
            for file in os.listdir(servicePath):
                if str.find(file, ".tar",-4) > 0:
                    archive_list[srv].append(archiving(os.path.join(servicePath, file)))
                    os.remove(os.path.join(servicePath, file))
    # export archives
    export(archive_list, os.path.join(config['logStoragePath'] + hostName))

def getTimeLabel():
    time_format = "%Y-%m-%d"
    return time.strftime(time_format, time.localtime())
    
def moveLogs(logsPath, backupPath, save_period):
    if os.path.exists(backupPath) is False:
        os.makedirs(backupPath)
    for root, dirs, files in os.walk(logsPath):
        relpath = root.replace(logsPath, "")
        if os.path.exists(backupPath + relpath) is False:
            os.makedirs(backupPath + relpath)
        for name in files:
            if _getModifyTime(os.path.join(root, name))  + save_period*24*3600 < time.time():
                shutil.copy2(os.path.join(root, name), os.path.join(backupPath +  relpath, name))
                os.remove(os.path.join(root, name))               
    
def _getModifyTime(filename):
    if filename is not None:
        fstat   = os.stat(filename)
        mtime   = fstat[stat.ST_MTIME]
        return mtime
    
def tar(archiveName, file):
    with tarfile.open(archiveName + '.tar', "a") as tar:
        tar.add(file, os.path.basename(file))        
    
def archiving(tarName):
    with open(tarName, 'rb') as f_in:
        with gzip.open(tarName + '.gz', 'wb') as f_out:
            f_out.writelines(f_in)
    return tarName + '.gz'

def export( archiveList, exportPath ):
    if os.path.exists(exportPath) is False:
        print('export path {0} is not found! Making new path'.format(str(exportPath)))
        os.makedirs(exportPath)
    for srv, path in archiveList.items():
        if os.path.exists(os.path.join(exportPath, srv)) is False:
            os.mkdir(os.path.join(exportPath, srv))
        for file in path: 
            shutil.copy2(file, os.path.join(exportPath, srv))
            os.remove(file)

if __name__ == '__main__':
    path    = sys.argv[1]    
    #path        = r"E:\logs.KOPF"
    backupLogs(path, config)    
    