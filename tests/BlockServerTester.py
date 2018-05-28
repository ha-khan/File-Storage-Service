# Unit Tests.
#!/usr/bin/env python

import sys
import os
import hashlib
import unittest


sys.path.append('gen-py')

# Thrift specific imports
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from shared.ttypes import *
from metadataServer.ttypes import *
from blockServer.ttypes import *
from blockServer import BlockServerService
from metadataServer import MetadataServerService

# Server Handlers.
from BSS import BSS
from MDD import MDD


def testDeleteIncorrectHash(res):
    if res.message != responseType.OK:
        print "testDeleteIncorrectHash: PASS"
    else:
        print "testDeleteIncorrectHash: FAIL"
    pass


if(__name__ == "__main__"):
    print "Starting BlockServer Tester"

    port = int(7080)  # NOTE: Make sure this and config.txt are equivalent.

    BlockServerServiceState = BSS(port)
    bHandler = BlockServerServiceState.ConnectAndReturnHandler()

    testDeleteIncorrectHash(bHandler.deleteBlock("Invalid Hash"))

'''
    # Variables Declared. 
    clientHandler = TritonTransfer(sys.argv)
    FileName = sys.argv[4]
    EveryFile = os.listdir(clientHandler.FileDirectory)
    clientHandler.storeLocalFiles(EveryFile) # NOTE: This might not be working correctly.

    # Try-Catch Blocks here.

    # Parse Ports
    port = int(clientHandler.ParsePort("block", "config.txt"))
    metaDataPort = int(clientHandler.ParsePort("metadata1", "config.txt"))

    # Instance  
    BlockServerServiceState = BSS(port)
    MetadataServerServiceState = MDD(metaDataPort)

    # Handlers
    # BlockServerServiceHandler = BlockServerServiceState.ConnectAndReturnHandler()
    MetadataServerServiceHandler = MetadataServerServiceState.ConnectAndReturnHandler()
'''
