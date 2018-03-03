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
from BSS import BSS
from MDD import MDD

# Abstract away some of the client functionality. 
from TritonTransfer import TritonTransfer
from UDC import UDC





def main():

    print "Starting Client"

    # Variables Declared.
    #clientHandler = TritonTransfer(sys.argv)
    cHandler = UDC(sys.argv)

    
    FileName = sys.argv[4]

    # Read all files in directory; and create a mapping of all available blocks.
    EveryFile = os.listdir(cHandler.clientHandler.FileDirectory)

    #clientHandler.storeLocalFiles(EveryFile)
    cHandler.storeLocalFiles(EveryFile)

    # Read config.txt, and parse ports of type int.
    blockPort = cHandler.parsePort("block","config.txt")#clientHandler.ParsePort("block", "config.txt")
    metaDataPort = cHandler.parsePort("metadata1","config.txt")#clientHandler.ParsePort("metadata1", "config.txt")  

    # State Controllers for Metadata/Block Servers.
    BlockServerServiceState = BSS(blockPort)
    MetadataServerServiceState = MDD(metaDataPort)

    # Connect to MetadataServer.
    MetadataServerServiceHandler = MetadataServerServiceState.ConnectAndReturnHandler()

    # Client Operation Exectution.
    # Create appropriate getters...
    if cHandler.clientHandler.OperationType == "upload":
        FileToSend = cHandler.generateFile(FileName)
        if FileToSend.status == responseType.OK:
            # BlockServiceServer Handler in Metadata is closed.
            response = cHandler.uploadFile(
                FileToSend, MetadataServerServiceHandler)
            if response.status == uploadResponseType.MISSING_BLOCKS:
                cHandler.uploadFileAndBlocks(BlockServerServiceState, FileName,
                                    response.hashList, FileToSend, MetadataServerServiceHandler)
            else:
                cHandler.output(response.status)
        else:
            print "ERROR"
    elif cHandler.clientHandler.OperationType == "download":
        FileData = MetadataServerServiceHandler.getFile(FileName)
        OrderedHashList = FileData.hashList
        # Check here if file already exist on loc using OrderedHashList
        MissingBlocks = cHandler.findMissingBlocks(MetadataServerServiceHandler, FileName)
        if MissingBlocks != None:
            if cHandler.downloadMissingBlocks(FileName, BlockServerServiceState, MissingBlocks):
                cHandler.combineBlocksToFile(FileName, OrderedHashList)
                print "OK"
            else:
                print "ERROR"
        else:
            print "ERROR"
        pass
    elif cHandler.OperationType == "delete":
        fileDel = cHandler.generateFile(FileName)
        response = MetadataServerServiceHandler.deleteFile(fileDel)
        if response.message == responseType.OK:
            print "OK"
        else:
            print "ERROR"
        pass
    else:
        print "ERROR"


if(__name__ == "__main__"):
    main()
