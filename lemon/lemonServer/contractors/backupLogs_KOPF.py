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
import logging
import subprocess
import distutils.dir_util as du


VERSION = '0.3.1'

service	    = 'KOPF'
export_dir  = '$export'
backup_dir  = '$backup_logs'
GZIP_PATH   = '.\\gzip.exe'

config  = {}


LOGGER     = ""

def initConfig():
    _cfg    = {
            'savePeriod': 7,    # за сколько дней от текущей даты архивировать логи
            'exportPath': r"\\localhost\e$\bkp\\"+service+"\\", 
            'localbackupPeriod' : 30 # за сколько дней хранить бэкапы на локальной машине
           }
    return _cfg 
    
def backupLogs( path, config ):
    LOGGER.info("STARTED")
    ####################################################################
    #    Creating dirs, constants
    #
    hostName    = socket.gethostname()
    backupPath  = os.path.join(path,'..',backup_dir,service)
    localExportPath  = os.path.join(backupPath, export_dir)
    if os.path.exists(backupPath) is False:
        os.makedirs(backupPath)
    if os.path.exists(localExportPath) is False:
        os.makedirs(localExportPath)
    
    #####################################################################

    LOGGER.info('MOVING')
    moveLogs( path, localExportPath, config['savePeriod'] )
    LOGGER.info('ARCHIVING')
    try:
        subprocess.check_call([GZIP_PATH, localExportPath, '--recursive','-9'])
    except subprocess.CalledProcessError as e:
        LOGGER.exception(e)
        return        
    LOGGER.info('EXPORT')
    export(localExportPath, config['exportPath'], hostName)
    LOGGER.info('Remove old backups')
    removeOldLocalBackups(backupPath, config['localbackupPeriod'])
    LOGGER.info('COMPLETED')    

def getTimeLabel(month=None, fromtime=None):
    time_format = "%Y-%m-%d"
    if month:
        time_format = "%Y-%m"
    return time.strftime(time_format, time.localtime(fromtime))
    
def moveLogs(logsPath, backupPath, save_period):
    for srv in os.listdir(logsPath):    
        for root, dirs, files in os.walk(os.path.join(logsPath,srv)):
            relpath = root.replace(os.path.join(logsPath, srv) + '\\', "")
            if relpath == root:
                relpath = ''            
            for name in files:
                file_mtime  = _getModifyTime(os.path.join(root, name))
                if file_mtime  + save_period*24*3600 < time.time():
                    month_dir   = getTimeLabel(True, file_mtime)                   
                    os.makedirs(os.path.join(backupPath, srv, month_dir, relpath),exist_ok=True)                    
                    shutil.move(os.path.join(root, name), os.path.join(backupPath,srv, month_dir,relpath,name))
                    LOGGER.info('MOVE: {0} to {1}'.format(os.path.join(root, name), os.path.join(backupPath,srv, month_dir,relpath,name)))              
        
def _getModifyTime(filename):
    if filename is not None:
        fstat   = os.stat(filename)
        mtime   = fstat[stat.ST_MTIME]
        return mtime
    
def archiving(name):    
    if name.startswith('.log', -4) is False:
        return
    LOGGER.info('GZIP {0}'.format(name + '.gz'))
    with open(name, 'rb') as f_in:
        with gzip.open(name + '.gz', 'wb') as f_out:
            f_out.writelines(f_in)
            LOGGER.info('GZIP {0} completed'.format(name + '.gz'))
    os.remove(name)        
    return name + '.gz'

def export( backupPath, exportPath, hostname ):
    os.makedirs(os.path.join(exportPath, hostname), exist_ok=True)
    try:
        copy_tree(backupPath, os.path.join(exportPath,hostname))
        resultCopyToBackup  = du.copy_tree(backupPath, os.path.join(backupPath,'..'))
        du.remove_tree(backupPath)
    except Exception as ex:
        LOGGER.exception(ex)
        return
    
def copy_tree(src, dst):
    os.makedirs(dst, exist_ok= True)
    src = os.path.normpath(src)
    for root, dirs, files in os.walk(src):
        relpath = root.replace(src + '\\', '')
        if relpath == src:
            relpath = ''        
        for name in dirs:
            os.makedirs(os.path.join(dst, relpath, name), exist_ok=True)
        for name in files:
            if os.path.exists(os.path.join(dst, relpath, name)):
                LOGGER.error('EXPORT FAILED: {0} is already exists'.format(os.path.join(dst, relpath, name)))
                raise Exception('File already exists')
            else:
                shutil.copy2(os.path.join(root, name), os.path.join(dst, relpath, name))
                LOGGER.info('EXPORT: {0} to {1}'.format(os.path.join(root, name), os.path.join(dst, relpath, name)))
    			
def removeOldLocalBackups(backupPath, backupsavePeriod):
    for root, dirs, files in os.walk(backupPath):
        for name in files:
            if _getModifyTime(os.path.join(root, name))  + backupsavePeriod*24*3600 < time.time():
                if name.startswith('.gz',-3):
                    LOGGER.info('REMOVE {0}'.format(os.path.join(root, name)))
                    os.remove(os.path.join(root, name))    
    				
def initLogger():
    logsDir    = 'logs'
    if os.path.exists(logsDir) is False:
        os.mkdir(logsDir)
    fileHandler     = logging.FileHandler('{0}/backup_logs_{1}.log'.format(logsDir, getTimeLabel()))
    _format  = "%(asctime)s\t %(name)s\t%(levelname)s\t%(message)s"
    fileFormatter   = logging.Formatter(_format)
    fileHandler.setFormatter(fileFormatter)
    consoleFormat   = "%(created)s\t%(levelno)s\t%(message)s"
    consoleFormatter    = logging.Formatter(consoleFormat)
    consoleHandler  = logging.StreamHandler()
    consoleHandler.setFormatter(consoleFormatter)
    logger  = logging.getLogger('BACKUP_LOGS')
    logger.addHandler(fileHandler)
    logger.addHandler(consoleHandler)
    logger.setLevel(logging.DEBUG)
    logger.propagate = True
    return logger
    
    
if __name__ == '__main__':
    LOGGER  = initLogger()
    try:
        if len(sys.argv) > 1:
            path    = sys.argv[1]
            if len(sys.argv) > 2:
                service = sys.argv[1]
                path    = sys.argv[2]
            config  = initConfig()    
            backupLogs(path, config)    
        else:
            LOGGER.error("Отсутствует аргумент Path командной строки")
    except Exception as e:
        LOGGER.exception(e)
        LOGGER.info('COMPLETED WITH ERRORS')   
           
   
    
