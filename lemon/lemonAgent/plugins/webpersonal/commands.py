#
#    Plugin: Webpersonal
#    file: commands
#

import importlib.machinery
import os

loader  = importlib.machinery.SourceFileLoader('webpersonal.controllers.webpersonalController',os.path.join(__file__,'..','controllers/webpersonalController.py'))
webpersonalController   =loader.load_module('webpersonal.controllers.webpersonalController')

COMMANDS    =  [
        [ 'copy_to',         webpersonalController.copy_to   ]
       ,[ 'switch_service_path', webpersonalController.switch_service_path   ]
       ,[ 'switch_front_path',   webpersonalController.switch_front_path     ]
    ]