#
#
#
#
import core
import os
import json
import re
from webpersonal.update import analize_distr 

def upload( req, res ):
    em  = core.getCoreInstance().getInstance('ENTITY_MANAGER')
    content_disposition = req.headers.get('Content-Disposition','').split(';')
    disposition_type    = content_disposition[0]
    file    = {}
    if disposition_type == 'attachment':
        for v in content_disposition:
            t   = v.split('=')
            if len(t) > 1:
                file[t[0]]   = t[1]
    else:
        res.send_response(406)  # Not acceptable
        res.end_headers()
        res.wfile.write("")
        return
    length  = int(req.headers.get('Content-Length',0))
    if 'filename' in file.keys():
        em.fileManager.writeFile(file['filename'], req.rfile, length)
        res.send_response(201)
        res.end_headers()
        res.wfile.write("")    
    else:
        res.send_response(406) 
        res.end_headers()  
        res.wfile.write("")
        
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
            result  = analize_distr( em.fileManager.getFilePath( distr_name ) )
            res.send_json( {'status': True, 'date': result} )
        else:
            res.send_error(404)            
              
def test( req, res):
    res.send_content('test')
    
    
    
