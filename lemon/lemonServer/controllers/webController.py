#
#
#
#
import core
import json
import uuid
import re
import os
import urllib
import time
from collections import OrderedDict
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
              
def check_status( req, res ):
    commands    = req.query.get('commands',[''])[0].split(' ')
    em  = core.getCoreInstance().getInstance('ENTITY_MANAGER')
    result  = {}
    for _id in commands:
        if _id:
            result[_id] = em.commandManager.getCommandStatus(_id)
    res.send_json(result)
    
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