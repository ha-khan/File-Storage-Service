#!/usr/bin/env python

import sys
import os
import hashlib


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
#from BSS import BSS
#from MDD import MDD

# Abstract away some of the client functionality. 
# from TritonTransfer import TritonTransfer
from UDC import UDC



def main():

    print "Starting Client"
    print "TO"

    # Variables Declared.
    cHandler = UDC(sys.argv)

    # Gather FileName. 
    FileName = sys.argv[4]

    # Read all files in directory; and create a mapping of all available blocks.
    EveryFile = os.listdir(cHandler.clientHandler.FileDirectory)

    # Store mapping of files in address space of client process. 
    cHandler.storeLocalFiles(EveryFile)

    if cHandler.clientHandler.OperationType == "upload":
        print "Upload"
        cHandler.upload(FileName)
    elif cHandler.clientHandler.OperationType == "download":
        print "Download"
        cHandler.download(FileName)
    elif cHandler.OperationType == "delete":
        print "Delete"
        cHandler.delete(FileName)
    else:
        print "INPUT ERROR"

if(__name__ == "__main__"):
    main()
