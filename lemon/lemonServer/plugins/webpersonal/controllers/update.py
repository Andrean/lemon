#
#    Update module. Contains functions for updated-related operations
#
#
import zipfile
import uuid
import os
import shutil
import pefile
import time

UPDATE  = { 'services': [], 'map': {}}

def analyze_distr(filepath):
    UPDATE['services'] = []
    if not zipfile.is_zipfile(filepath):
        return
    zdistr  = zipfile.ZipFile(filepath)
    temp_dir    = os.path.join(os.path.dirname(filepath),'temp_'+str(uuid.uuid4()))
    try:
        os.makedirs(temp_dir)
    except:
        return
    zdistr.extractall(temp_dir)
    services    = []
    try:
        for _dir in os.listdir(temp_dir):
            filelist = []
            binfolder   = _dir
            if _dir == 'Front':
                binfolder   = os.path.join(binfolder, 'bin')
            for file in os.listdir(os.path.join(temp_dir, binfolder)):
                try:
                    filelist.append( { 'name': file, 'version': None } )
                    path    = os.path.join(temp_dir, binfolder, file)
                    if os.path.isfile(path):
                        filelist[-1]['version'] = getFileVersion(path)
                except pefile.PEFormatError:
                    pass                
            services.append( { 'service': _dir, 'filelist': filelist })
    finally:
        shutil.rmtree(temp_dir)
    UPDATE['services'] = services
    return services

def prepare_services( services, distr ):
    if not zipfile.is_zipfile(distr):
        return
    zdistr  = zipfile.ZipFile(distr)
    temp_dir    = os.path.join(os.path.dirname(distr),'temp_'+str(uuid.uuid4()))
    try:
        os.makedirs(temp_dir)
    except:
        return
    zdistr.extractall(temp_dir)
    update_timestamp   = time.strftime('%Y.%m.%d_%H.%M')    
    filelist    = []
    try:
        for _dir in os.listdir(temp_dir):
            if _dir in services:
                os.makedirs(os.path.join(temp_dir, _dir, update_timestamp))
                for item in os.listdir( os.path.join(temp_dir, _dir) ):
                    if item == update_timestamp:
                        continue
                    shutil.move( os.path.join(temp_dir, _dir, item) , os.path.join(temp_dir, _dir, update_timestamp) )
                    
                zsrv    = zipfile.ZipFile(os.path.join(temp_dir, '..', _dir+".zip"),'w')
                zipdir( os.path.join(temp_dir, _dir), zsrv)
                zsrv.close()
                filelist.append( {'service' : _dir, 'file': _dir+".zip", 'stamp': update_timestamp} )                
    finally:
        shutil.rmtree(temp_dir)
    return filelist 

def getSettingsArchive(filename, settings, cfg_path):
    downloads   = 'files'
    os.makedirs(downloads,exist_ok=True);
    zsettings   = zipfile.ZipFile(os.path.join(downloads,filename), 'w')
    for file in os.listdir(cfg_path):
        for stg in settings:
            if stg['fileName'] == file:
                zsettings.write(os.path.join(cfg_path,file), stg['name'])

def getFileVersion(path):
    def LOWORD(dword):
        return str(dword & 0x0000ffff)
    def HIWORD(dword): 
        return str(dword >> 16)
    try:
        pe = pefile.PE(path)
        if not pe.is_dll() and not pe.is_exe() and not pe.is_driver():
            return None
        #print PE.dump_info()
    
        ms = pe.VS_FIXEDFILEINFO.ProductVersionMS
        ls = pe.VS_FIXEDFILEINFO.ProductVersionLS
        pe.close()
        return "{0}.{1}.{2}.{3}".format(HIWORD (ms), LOWORD (ms), HIWORD (ls), LOWORD (ls))
    except:
        return ''    

def zipdir(path, zip):
    rootlen = len(os.path.dirname(path)) + 1
    for root, dirs, files in os.walk(path):
        for file in files:
            fn = os.path.join(root, file)
            zip.write(fn,fn[rootlen:])
