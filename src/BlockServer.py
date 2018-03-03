#!/usr/bin/env python

import sys

sys.path.append('gen-py')


# from shared import responseType
from blockServer import BlockServerService
from blockServer.ttypes import *
from shared.ttypes import *

from thrift import Thrift
from thrift.transport import TSocket
from thrift.server import TServer
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol



# Review the files in the thrift folder titled blockServer.thrift and shared.thrift. 
#
# This file contains the implementation code for the Blockfile Server, which essentially keeps track
# of a dictionary that contains (hn) -> {Bn}, where each hn is the key and hashed signature for the 
# block of bytes, that is the value. 
#
class BlockServerHandler():

    def __init__(self):
        self.blocks = {}  # Hash -> Block
        pass

    def storeBlock(self, hashBlock):
        if not hashBlock.hash in self.blocks:
            self.blocks[hashBlock.hash] = hashBlock
            r = response()
            r.message = responseType.OK
            return r
        else:
            r = response()
            r.message = responseType.ERROR
            return r
        pass

    # NOTE: In case of hash (key) not in storage, return None.
    def getBlock(self, hash):
        if hash in self.blocks:
            return self.blocks[hash]
        else:
            return None
        pass

    def deleteBlock(self, hash):
        if hash in self.blocks:
            del self.blocks[hash]
            r = response()
            r.message = responseType.OK
            return r
        else:
            r = response()
            r.message = responseType.ERROR
            return r
        pass

    def hasBlock(self, hash):
        if hash in self.blocks:
            return True
        else:
            return False
        pass


def readServerPort(fPath):
    f = open(fPath)
    for l in f:
        if "block" in l:
            p1 = l.index(":") + 2
            p2 = (len(l))
            return l[p1:p2]
    pass


# NOTE: Add Try Catch
def main():
    if (len(sys.argv) < 2):
        print "Invocation  <config_file>"
        exit(-1)

    config_path = sys.argv[1]
    print "Initializing block server"
    handler = BlockServerHandler()

    # Retrieve the port number from the config file so that you could strt the server
    port = int(readServerPort(config_path))

    # Define parameters for thrift server
    processor = BlockServerService.Processor(handler)
    transport = TSocket.TServerSocket(port=port)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    # Create a server object
    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
    print "Starting server on port : ", port
    server.serve()



#  Server Running.  Restructure this...
#
if __name__ == "__main__":
    main()
