'''
Created on 19.06.2013

@author: vau
'''

from socketserver import ThreadingMixIn
from xmlrpc.server import SimpleXMLRPCServer
from exception.lemonException import ServerExitException

class xmlrpcListener( ThreadingMixIn, SimpleXMLRPCServer ):
    pass

class XMLRPCExitException(ServerExitException):
    pass
    