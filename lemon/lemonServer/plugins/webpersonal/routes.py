



import importlib.machinery
import os

def load_controller(controller):
    module_name = __name__ + '.' + controller
    return importlib.machinery.SourceFileLoader(module_name, os.path.join(__file__,'..','controllers',controller + '.py')).load_module(module_name)

webController   = load_controller('webcontroller')

WEB_ROUTES  = [
     [  'POST', r'^/update/distr$', webController.post_distr                ]
    ,[  'POST', r'^/update/copy_to_agents$', webController.copy_services_to_agents  ]
    ,[  'POST', r'^/update/switch_services$', webController.switch_services ]
    ,[  'POST', r'^/update/switch_fronts$', webController.switch_fronts     ]
    ]

def get(method, _filter=None):
    if not _filter:
        return [x for x in WEB_ROUTES if x[0] == method]
    if _filter == 'web':
        return [x for x in WEB_ROUTES if x[0] == method]