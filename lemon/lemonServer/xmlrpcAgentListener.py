'''
Created on 19.06.2013

@author: vau
'''

from agentInterface import AgentListener
from socketserver import ThreadingMixIn
from xmlrpc.server import SimpleXMLRPCServer

class xmlrpcAgentListener(ThreadingMixIn, SimpleXMLRPCServer ):
    pass
