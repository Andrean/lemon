'''
Created on 19.06.2013

@author: vau
'''

from agentInterface import AgentHandler
from socketserver import ThreadingMixIn
from xmlrpc.server import SimpleXMLRPCServer
from exception.lemonException import LemonException

class xmlrpcAgentListener(ThreadingMixIn, SimpleXMLRPCServer ):
    pass

class XMLRPCExitException(LemonException):
    pass
    