

import core
import uuid
import time
import re
import json
import os
from collections import OrderedDict
from entity_manager import commands
import importlib.machinery
update  = importlib.machinery.SourceFileLoader('plugins.webpersonal.update',os.path.join(__file__,'..','update.py')).load_module('plugins.webpersonal.update')

def post_distr( req, res ):
    em  = core.getCoreInstance().getInstance('ENTITY_MANAGER')    
    db  = core.getCoreInstance().getInstance('STORAGE').getInstance()
    db.set_default_collection('update.sessions')
    session = {
               'session_id': str(uuid.uuid4()), 
               'distr': {'filename': ''}, 
               'services':[],
               'stamp': '',
               'info_system':'',
               'history': {'begin': time.time(), 'load_distr': None, 'distribute_files': None, 'switch_services': None, 'switch_fronts': None, 'end': None } 
               }
    content_type    = req.headers.get('Content-Type','text/plain;charset=utf-8')
    content_length  = int(req.headers.get('Content-Length',0))
    if content_length == 0:
        res.send_error(411)
        return      
    charset         = 'utf-8'
    match = re.match(r';charset=([\w-]+)',content_type)
    if match:   
        charset = match.groups[1]        
    body    = json.loads(str(req.rfile.read(content_length), charset))
    if 'distr' in body.keys():        
        distr_name  = body['distr']['name']
        if em.fileManager.isExistsFile( distr_name ):
            # Запускаем процедуру проверки дистрибутива
            # после ее выполнения отправляем json с результатами
            session['distr']['name']    = distr_name
            session['info_system']      = body['info_system']
            db.insert(session)
            result  = update.analyze_distr( em.fileManager.getFilePath( distr_name ) )
            if not result:
                res.send_json( {'status': False, 'session_id': session['session_id'] } )
                return
            session = db.findOne({'session_id': session['session_id']})
            session['history']['load_distr'] = time.time()
            db.save(session)
            res.send_json( {'status': True, 'data': result, 'session_id': session['session_id']} )
        else:
            res.send_error(404) 
            
def copy_services_to_agents( req, res):
    em  = core.getCoreInstance().getInstance('ENTITY_MANAGER')
    content_type    = req.headers.get('Content-Type','text/plain;charset=utf-8')
    content_length  = int(req.headers.get('Content-Length',0))
    if content_length == 0:
        res.send_error(411)
        return      
    charset         = 'utf-8'
    match = re.match(r';charset=([\w-]+)',content_type)
    if match:   
        charset = match.groups[1]        
    body    = json.loads(str(req.rfile.read(content_length), charset))
    # body вида { 'session_id': String, 'services':[]}
    db  = core.getCoreInstance().getInstance('STORAGE').getInstance()
    db.set_default_collection('update.sessions')
    session = db.findOne({'session_id': body['session_id']})
    if session is None:
        res.send_error(403)
        return
    
    try:   
        # Возвращает list вида [{'service': name, 'file': file,'stamp':stamp}]
        
        service_list    = update.prepare_services( body['services'], em.fileManager.getFilePath( session['distr']['name'] ) )
        if service_list is None:
            raise ValueError
        for srv in service_list:
            srv['link'] = em.fileManager.createVirtualLink(srv['file'])
        print(service_list)
        (commands_id, stamp, tags)    = getServicesByTag(service_list, session['info_system'])    
        (scommands_id, stamp, stags)   = getSettingsByService(service_list, session['info_system'], 'D:/cfg/'+session['info_system']+'/settings')
        commands_id.extend(scommands_id) 
        tags.extend(stags)
        tags    = list(OrderedDict.fromkeys(tags))   
        session['services'] = body['services']
        session['stamp']    = stamp
        session['history']['distribute_files']  = time.time()        
        db.save(session)
        res.send_json( {'status': True, 'session_id':session['session_id'], 'stamp':stamp, 'tags':tags, 'check_link': '/commands/status?commands=' + (','.join(commands_id))} )    
    except:        
        res.send_error(406)
        
def getServicesByTag(srv_list, system_name):
    #    Вид карты сервиса:
    #    [
    #        { 'tag': tag, 'services': [ {'name':'Service1','settings':[]} ], 'topology': [ 'server1', 'server2', .. ], 'path': service_working_path   },
    #        { ... },
    #    ]
    #
    em  = core.getCoreInstance().getInstance('ENTITY_MANAGER')
    db  = core.getCoreInstance().getInstance('STORAGE').getInstance()
    db.set_default_collection( 'service_map' )
    system_map = db.findOne({'type': 'map', 'info_system': system_name})
    commands_id    = []
    stamp           =''
    tags    = []
    for group in system_map['map']:            
        args    = []
        for srv in group['services']:
            for x in srv_list:
                if srv['name'] == x['service']:
                    args.append({'link': x['link'],'path': group['path']})
                    stamp   = x['stamp']
        if len(args) > 0:
            commands_id.append( em.sendCommand(commands['copy_to'], args, [group['tag']] ) )
            tags.append(group['tag'])
    return (commands_id, stamp, tags)
    
def getSettingsByService(srv_list, system_name, cfg_path):
    em  = core.getCoreInstance().getInstance('ENTITY_MANAGER')
    db  = core.getCoreInstance().getInstance('STORAGE').getInstance()
    db.set_default_collection( 'service_map' )
    system_map = db.findOne({'type': 'map', 'info_system': system_name})
    commands_id    = []
    stamp           =''
    tags            = []
    for group in system_map['map']:            
        args    = []
        for srv in group['services']:
            for x in srv_list:
                if srv['name'] == x['service']:
                    update.getSettingsArchive(srv['name']+'_settings.zip', srv['settings'], cfg_path)
                    link   = em.fileManager.createVirtualLink(srv['name']+'_settings.zip')
                    path   = os.path.join(group['path'],srv['name'],x['stamp'],'Settings')
                    if srv['name'] == 'Front':
                        path   = os.path.join(group['path'],srv['name'],x['stamp'],'bin','Settings')
                    stamp       = x['stamp']
                    args.append({'link': link, 'path': path})                        
        if len(args) > 0:
            commands_id.append( em.sendCommand(commands['copy_to'], args, [group['tag']] ) )
            tags.append(group['tag'])
    return (commands_id, stamp, tags)
        

def switch_services( req ,res ):
    content_type    = req.headers.get('Content-Type','text/plain;charset=utf-8')
    content_length  = int(req.headers.get('Content-Length',0))
    if content_length == 0:
        res.send_error(411)
        return      
    charset         = 'utf-8'
    match = re.match(r';charset=([\w-]+)',content_type)
    if match:   
        charset = match.groups[1]        
    body    = json.loads(str(req.rfile.read(content_length), charset))
    # body вида {'session_id': String}
    # последовательное переключение сервисов
    em  = core.getCoreInstance().getInstance('ENTITY_MANAGER')
    db  = core.getCoreInstance().getInstance('STORAGE').getInstance()
    db.set_default_collection('update.sessions')
    session = db.findOne({'session_id':body['session_id']})
    if session is None:
        res.send(403)
        return
    db.set_default_collection( 'service_map' )
    system_map = db.findOne({'type':'map','info_system':session['info_system']})
    tags = {}
    switch_info = {'port': system_map['sm_port'], 'items':[]}
    for _map in system_map['map']:
        for srv in _map['services']:
            if srv['name'] in session['services']:                
                tags[_map['tag']] = True
                switch_info['items'].append({'service': srv['name'], 'path': _map['path'] + '\\' + srv['name']+ '\\' + session['stamp'] })
    session['history']['switch_services'] = time.time()
    db.save(session)
    db.set_default_collection( 'agents')
    if 'Front' in session['services']:
        session['services'].remove('Front')
    command_id  = em.sendCommand(commands['switch_service_path'], switch_info, tags.keys())
    res.send_json( {'status': True, 'session_id':session['session_id'], 'tags':list(tags.keys()), 'check_link': '/commands/status?commands='+command_id } )
            
def switch_fronts( req ,res ):
    content_type    = req.headers.get('Content-Type','text/plain;charset=utf-8')
    content_length  = int(req.headers.get('Content-Length',0))
    if content_length == 0:
        res.send_error(411)
        return      
    charset         = 'utf-8'
    match = re.match(r';charset=([\w-]+)',content_type)
    if match:   
        charset = match.groups[1]        
    body    = json.loads(str(req.rfile.read(content_length), charset))
    # body вида {'session_id': String}
    # последовательное переключение сервисов
    em  = core.getCoreInstance().getInstance('ENTITY_MANAGER')
    db  = core.getCoreInstance().getInstance('STORAGE').getInstance()
    db.set_default_collection('update.sessions')
    session = db.findOne({'session_id':body['session_id']})
    if session is None:
        res.send(403)
        return
    db.set_default_collection( 'service_map' )
    system_map = db.findOne({'type':'map','info_system':session['info_system']})
    tags = {}
    switch_info = {'iis_site':system_map['iis_site'], 'items': []}
    for _map in system_map['map']:
        if 'Front' in session['services']:                
            tags[_map['tag']] = True
            switch_info['items'].append({'service':'Front', 'path': _map['path'] + '/Front/' + session['stamp']})
    if 'Front' in session['services']:
        session['history']['switch_fronts'] = time.time()
        db.save(session)
        command_id  = em.sendCommand(commands['switch_front_path'], switch_info, tags.keys())
        res.send_json( {'status': True, 'session_id':session['session_id'], 'tags':list(tags.keys()),'check_link': '/commands/status?commands='+command_id } )
    else:
        res.send_json( {'status': False, 'session_id':session['session_id']})