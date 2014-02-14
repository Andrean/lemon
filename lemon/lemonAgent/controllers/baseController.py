'''
Created on 20 янв. 2014 г.

@author: Andrean
'''
import core
import os
import shutil
import zipfile
import subprocess

def get_self_info(*args):
    print('get_self_info completed')
    
def update_agent(*args):
    # create .cmd_id.lock file for detecting update
    command = args[0]
    if os.path.exists('.{0}.lock'.format(command['id'])):
        os.remove('.{0}.lock'.format(command['id']))
        # Нужно отправить информацию об успешном обновлении
        return
    with open( '.{0}.lock'.format(command['id']), 'w' ) as f:
        f.write('1')
    try:
        rh  = core.getCoreInstance().getInstance('INTERFACE').getHandler()
        file = rh.get_file('/files?file={0}'.format(command['args']['link']))
        if file and file['type'] == 'attachment':
            if os.path.exists('files/update'):
                shutil.rmtree('files/update')
            os.makedirs('files/update', exist_ok=True)                
            with open('files/'+file['filename'],'wb') as f:
                shutil.copyfileobj(file['file'], f, file['length'])        
            zipfile.ZipFile('files/'+file['filename']).extractall('files/update')
            os.remove('files/'+file['filename'])
            subprocess.check_output(['python','files/update/__update__.py'],universal_newlines=True,timeout=60,shell=True)
            core.getCoreInstance().restart()
    except:
        os.remove('.{0}.lock'.format(command['id']))
        raise
        