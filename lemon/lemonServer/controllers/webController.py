#
#
#
#
import core
import os

def upload( req, res ):
    #em  = core.getCoreInstance().getInstance('ENTITY_MANAGER')
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
        os.makedirs('files', exist_ok=True)
        with open('files/' + file['filename'], 'wb') as wstream:
            buf_length  = 40000
            while length > 0:
                write_len   = buf_length if length > buf_length else length
                buffer  = req.rfile.read( write_len )
                wstream.write(buffer)
                length -= buf_length
            wstream.close()
        res.send_response(201)
        res.end_headers()
        res.wfile.write("")
    else:
        res.send_response(406) 
        res.end_headers()  
        res.wfile.write("")  
              
def test( req, res):
    res.send_content('test')
    
    
    
