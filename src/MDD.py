from thrift import Thrift
from thrift.transport import TSocket
from thrift.server import TServer
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from metadataServer.ttypes import *
from metadataServer import MetadataServerService

# Class that helps initialize the handler and connect it to the Metadata Server
# And allows the client process to make RPC to the Metadata Server. 
class MDD():
    def __init__(self, port):
        self.port = port
        self.transport = None
        self.protocol = None
        self.client = None
        pass

    def ConnectAndReturnHandler(self):
        self.transport = TSocket.TSocket('localhost', self.port) # localhost -> let user decide for mod..
        self.transport = TTransport.TBufferedTransport(self.transport)
        self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        self.client = MetadataServerService.Client(self.protocol)
        self.transport.open()
        return self.client
        pass

