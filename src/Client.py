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

# Abstract away some of the client functionality. 
# from TritonTransfer import TritonTransfer
from UDC import UDC

def OutputResponseToConsole(response):
    if response == uploadResponseType.MISSING_BLOCKS:
        print "MISSING BLOCKS"
    elif response == uploadResponseType.FILE_ALREADY_PRESENT:
        print "FILE ALREADY PRESENT"
    elif response == uploadResponseType.OK:
        print "OK"
    elif response == uploadResponseType.ERROR:
        print "ERROR"
    else:
        print "UNKNOWN RESPONSE"

def main():

    print "Starting Client"

    cHandler = UDC(sys.argv)

    FileName = sys.argv[4]

    OperationType = sys.argv[3]

    # Read all files in directory; and create a mapping of all available blocks.
    EveryFile = os.listdir(cHandler.clientHandler.FileDirectory)

    # Store mapping of files in address space of client process. 
    cHandler.storeLocalFiles(EveryFile)

    if OperationType == "upload":
        print "Upload"
        result = cHandler.upload(FileName)
        OutputResponseToConsole(result)
    elif OperationType == "download":
        print "Download"
        result = cHandler.download(FileName)
        OutputResponseToConsole(result)
    elif OperationType == "delete":
        print "Delete"
        cHandler.delete(FileName)
    else:
        print "INPUT ERROR"

if(__name__ == "__main__"):
    main()
