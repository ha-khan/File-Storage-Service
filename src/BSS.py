from thrift import Thrift
from thrift.transport import TSocket
from thrift.server import TServer
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from blockServer.ttypes import *
from blockServer import BlockServerService


# Class that helps initialize the handler and connect it to the Metadata Server
# And allows the client process to make RPC to the Blockfile Server.   
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



