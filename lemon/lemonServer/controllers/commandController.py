
def get_commands( req, res ):
    res.send_header('Content-Type','text/plain;charset=utf-8')
    res.wfile.write(bytes("This is command!",'utf-8'))