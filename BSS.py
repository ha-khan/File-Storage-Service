from thrift import Thrift
from thrift.transport import TSocket
from thrift.server import TServer
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from blockServer.ttypes import *
from blockServer import BlockServerService


# Make an abstract base class? 
class BSS():
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
        self.client = BlockServerService.Client(self.protocol)
        self.transport.open()
        return self.client
        pass

    def CloseConnection(self):
	self.transport.close()
	pass



