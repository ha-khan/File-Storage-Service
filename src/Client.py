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
from TritonTransfer import TritonTransfer

# Driver program on the client side.



# main() functions.
def UploadFileAndBlocks(BlockServerServiceState,  clientHandler, FileName, HashList, FileToSend, MetadataServerServiceHandler):
    BlockServerServiceHandler = BlockServerServiceState.ConnectAndReturnHandler()
    # Need to close and reopen.
    clientHandler.UploadFileBlocks(
        FileName, HashList, BlockServerServiceHandler)
    BlockServerServiceState.CloseConnection()  # Connection is closed.
    secondResponse = clientHandler.UploadFile(
        FileToSend, MetadataServerServiceHandler)
    clientHandler.OutputResponseToConsole(secondResponse.status)
    pass


# NOTE: Assumption is that Blocks are local and stored in clientHandler.FileBlockList
#       And that the guide to build the filr back up is in OrderedHashList.
# OK.
def CombineBlocksToFile(clientHandler, FileName, OrderedHashList):
    hLIST = []
    for hash in OrderedHashList:  # change this.
        for key in clientHandler.FileBlockList:
            if hash in clientHandler.FileBlockList[key]:
                hLIST.append(clientHandler.FileBlockList[key][hash].block)
                break  # So to not copy more
    fd = open(clientHandler.FileDirectory + FileName, "wb")
    temp = "".join([str(x) for x in hLIST])
    fd.write(temp)
    fd.close()
    pass


# NOTE: Returns a list of missing blocks.
def FindMissingBlocks(MetadataServerServiceHandler, FileName, clientHandler):
    # Returns File Obj.
    responseFile = MetadataServerServiceHandler.getFile(FileName)
    if responseFile.status == responseType.OK:
        # Total Blocks that make up this file.
        BlockServerList = responseFile.hashList
        # Need to check whether FileName is saved..NOTE: sec ar == []
        MissingBlocks = GetBlocksFromList(BlockServerList, clientHandler)
        return MissingBlocks
    else:
        return None
    pass


# NOTE: OK.
def CheckUploadResponseStatus(uResponse):
    return uResponse.status == uploadResponseType.OK
    pass


def PrintStoredBlocks(clientHandler):
    for key in clientHandler.FileBlockList:
        for h in clientHandler.FileBlockList[key]:
            print clientHandler.FileBlockList[key][h].hash
    pass


# NOTE: OK.
def FileOK(response):
    return response.message == responseType.OK


# NOTE: Returns a list of blocks that were NOT locally stored in cHandler.
def GetBlocksFromList(HashList, cHandler):
    MissingBlocks = []
    Flag = False
    for hash in HashList:
        for key in cHandler.FileBlockList:
            if hash in cHandler.FileBlockList[key]:
                Flag = True
        if not Flag:
            MissingBlocks.append(hash)
        Flag = False  # For next round.
    return MissingBlocks
    pass


# NOTE: Need to test out hashBLK Return
def DownloadMissingBlocks(clientHandler, FileName, BlockServ, MissingBlocks):
    BlockServerHandler = BlockServ.ConnectAndReturnHandler()
    # This overwrites the data...deleting it.
    if not FileName in clientHandler.FileBlockList:
        clientHandler.FileBlockList[FileName] = {}

    for blk in MissingBlocks:
        hashBlk = BlockServerHandler.getBlock(blk)
        if hashBlk != None:
            clientHandler.FileBlockList[FileName][blk] = hashBlk
        else:
            return False
    BlockServ.CloseConnection()
    return True
    pass


# TODO:  MetaData and MetaData->BlockServer.
def main():

    # print "Starting Client"

    # Variables Declared.
    clientHandler = TritonTransfer(sys.argv)
    FileName = sys.argv[4]

    # Read all files in directory; and create a mapping of all available blocks.
    EveryFile = os.listdir(clientHandler.FileDirectory)
    clientHandler.storeLocalFiles(EveryFile)

    # Read config.txt, and parse ports of type int.
    blockPort = clientHandler.ParsePort("block", "config.txt")
    metaDataPort = clientHandler.ParsePort(
        "metadata1", "config.txt")  # Would need to change for Part2

    # State Controllers for Metadata/Block Servers.
    BlockServerServiceState = BSS(blockPort)
    MetadataServerServiceState = MDD(metaDataPort)

    # Connect to MetadataServer.
    MetadataServerServiceHandler = MetadataServerServiceState.ConnectAndReturnHandler()

    # Client Operation Exectution.
    if clientHandler.OperationType == "upload":
        FileToSend = clientHandler.GenerateFile(FileName)
        if FileToSend.status == responseType.OK:
            # BlockServiceServer Handler in Metadata is closed.
            response = clientHandler.UploadFile(
                FileToSend, MetadataServerServiceHandler)
            if response.status == uploadResponseType.MISSING_BLOCKS:
                UploadFileAndBlocks(BlockServerServiceState,  clientHandler, FileName,
                                    response.hashList, FileToSend, MetadataServerServiceHandler)
            else:
                clientHandler.OutputResponseToConsole(response.status)
        else:
            print "ERROR"
    elif clientHandler.OperationType == "download":
        FileData = MetadataServerServiceHandler.getFile(FileName)
        OrderedHashList = FileData.hashList
        # Check here if file already exist on loc using OrderedHashList
        MissingBlocks = FindMissingBlocks(
            MetadataServerServiceHandler, FileName, clientHandler)
        if MissingBlocks != None:
            if DownloadMissingBlocks(clientHandler, FileName, BlockServerServiceState, MissingBlocks):
                CombineBlocksToFile(clientHandler, FileName, OrderedHashList)
                print "OK"
            else:
                print "ERROR"
        else:
            print "ERROR"
        pass
    # NOTE: Fix this
    elif clientHandler.OperationType == "delete":
        fileDel = clientHandler.GenerateFile(FileName)
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
