'''
Created on 18.06.2013

@author: vau
'''

import os

CONFIG_PATH = 'conf'
CONFIG_FILE = CONFIG_PATH + '/server.conf'

def writeDefaultConfig(config):
    config.add_section('STORAGE')
    storageConfig                   = config['STORAGE']
    storageConfig['data_path']      = 'data/storage/'
    config.add_section('WEBSTORAGE')
    webstorageConfig                = config['WEBSTORAGE']
    webstorageConfig['data_path']   = 'data/webstorage/'
    config.add_section('LOGGING')
    loggingConfig                   = config['LOGGING']
    loggingConfig['file']           = CONFIG_PATH + '/logging.conf'
    if not os.path.exists(CONFIG_PATH):
        os.makedirs(CONFIG_PATH)
    with open(CONFIG_FILE,'w') as configFile:        
        config.write(configFile)