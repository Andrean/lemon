'''
Created on 19.06.2013

@author: vau
'''

from agentInterface import AgentHandler
from socketserver import ThreadingMixIn
from xmlrpc.server import SimpleXMLRPCServer
from exception.lemonException import ServerExitException

class xmlrpcAgentListener(ThreadingMixIn, SimpleXMLRPCServer ):
    pass

class XMLRPCExitException(ServerExitException):
    pass
    