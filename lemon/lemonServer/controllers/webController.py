#
#
#
#
import core
import os
import json
import re
import webpersonal.update as update
import urllib
from entity_manager import commands

def upload( req, res ):
    em  = core.getCoreInstance().getInstance('ENTITY_MANAGER')
    content_disposition = req.headers.get('Content-Disposition','').split(';')
    disposition_type    = content_disposition[0]
    file    = {}
    if disposition_type == 'attachment':
        for v in content_disposition:
            t   = v.split('=')
            if len(t) > 1:
                file[t[0]]   = urllib.parse.unquote_plus(t[1])
    else:
        res.send_error(406)
        return
    length  = int(req.headers.get('Content-Length',0))
    if 'filename' in file.keys():
        em.fileManager.writeFile(file['filename'], req.rfile, length)
        res.send_content(code=201, content='{}')
        return
    else:
        res.send_error(406)  
        return
    
def post_distr( req, res ):
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
    if 'distr' in body.keys():        
        distr_name  = body['distr']['name']
        if em.fileManager.isExistsFile( distr_name ):
            # Запускаем процедуру проверки дистрибутива
            # после ее выполнения отправляем json с результатами
            result  = update.analyze_distr( em.fileManager.getFilePath( distr_name ) )
            if not result:
                res.send_json( {'status': False } )
                return
            res.send_json( {'status': True, 'data': result} )
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
    # body вида { 'system': information_system_name, 'services': ['Front', 'ImportService'], 'distr': {'name': file }}
    try:   
        # Возвращает list вида [{'service': name, 'file': file}]
        service_list    = update.prepare_services( body['services'], em.fileManager.getFilePath( body['distr']['name'] ) )
        if service_list is None:
            raise ValueError
        for srv in service_list:
            srv['link'] = em.fileManager.createVirtualLink(srv['file'])
        
        #    Вид карты сервиса:
        #    [
        #        { 'tag': tag, 'services': [ 'Service1','Service2' ], 'topology': [ 'server1', 'server2', .. ],    },
        #        { ... },
        #    ]
        #
        db  = core.getCoreInstance().getInstance('STORAGE').getInstance()
        db.set_default_collection( 'update' )
        system_map = db.findOne({'type': 'map', 'info_system': body['system']})
        if not system_map:
            res.send_json(code=404,content={'status': False, 'msg': 'Information system not found' })
            return
        for group in system_map['map']:
            em.sendCommand(commands.copy_distr, [x for x in service_list if x['service'] in group['services']], group.tag )
        res.send_json( {'status': True, 'check_link': '/update/status'} )    
    except:
        res.send_error(406)
              
def test( req, res):
    res.send_content('test')
    
def get_agents( req, res ):
    em  = core.getCoreInstance().getInstance('ENTITY_MANAGER')
    agents  = [x for x in em.agentManager.get()]
    res.send_json( agents )

def post_agents( req, res ):
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
    for record in body:
        agent_id = record.get('agent_id')
        del_tag  = record.get('del_tag',None)
        add_tag  = record.get('add_tag', None)
        if add_tag:
            em.tagManager.assignTag(agent_id, add_tag)
        if del_tag:
            em.tagManager.removeTag(agent_id, del_tag)
    res.send_json( {'status': True} )
        
    
    
    
