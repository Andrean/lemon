'''
Created on 13.06.2013

@author: vau
'''
import server
import webInterfaceListener
import main_config
import configparser
import logging.config


if __name__ == '__main__':
    
    config  = configparser.ConfigParser()
    config.read(main_config.CONFIG_FILE)
    if len(config.sections()) < 1:
        main_config.writeDefaultConfig(config)
    logging.config.fileConfig(config['LOGGING']['file'])
    
    agentServerInstance      = server.Server(20);
    httpInterfaceInstance    = webInterfaceListener.httpListener();
    
    agentServerInstance.start();
    httpInterfaceInstance.start();