# Class definition file, which will abstract away functionality written in client.
# To make client less intensive. Will act as a wrapper for TritonTransfer, which is my legacy code...
# 
# 
# 


import sys
import os
import hashlib

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

# Server Handlers.
from BSS import BSS
from MDD import MDD

# Abstract away some of the client functionality. 
from TritonTransfer import TritonTransfer


class UDC():
    def __init__(self, argumentList):
        self.clientHandler = TritonTransfer(sys.argv)
        pass

    def storeLocalFiles(self, fileList):
        self.clientHandler.storeLocalFiles(fileList)
        pass

    def parsePort(self, serverType, configFile):
        return self.clientHandler.ParsePort(serverType, configFile)
    
    def uploadFileAndBlocks(self, BlockServerServiceState, FileName, HashList, FileToSend, MetadataServerServiceHandler):
        BlockServerServiceHandler = BlockServerServiceState.ConnectAndReturnHandler()
        self.clientHandler.UploadFileBlocks(FileName, HashList, BlockServerServiceHandler)
        BlockServerServiceState.CloseConnection()
        secondResponse = self.clientHandler.UploadFile(FileToSend, MetadataServerServiceHandler)
        self.clientHandler.OutputResponseToConsole(secondResponse.status)
        pass

    def generateFile(self, FileName):
        return self.clientHandler.GenerateFile(FileName)
        
    def uploadFile(self, FileToSend, MDS):
        return self.clientHandler.UploadFile(FileToSend, MDS)
    
    def output(self, response):
        self.clientHandler.OutputResponseToConsole(response)

    def findMissingBlocks(self, MetadataServerServiceHandler, FileName):
        # Returns File Obj.
        responseFile = MetadataServerServiceHandler.getFile(FileName)
        if responseFile.status == responseType.OK:
            # Total Blocks that make up this file.
            BlockServerList = responseFile.hashList
            MissingBlocks = self.__GetBlocksFromList(BlockServerList)
            return MissingBlocks
        else:
            return None
        pass

    # NOTE: Returns a list of blocks that were NOT locally stored in cHandler.
    def __GetBlocksFromList(self, HashList):
        MissingBlocks = []
        Flag = False
        for hash in HashList:
            for key in self.clientHandler.FileBlockList:
                if hash in self.clientHandler.FileBlockList[key]:
                    Flag = True
            if not Flag:
                MissingBlocks.append(hash)
            Flag = False  # For next round.
        return MissingBlocks
        pass

    # NOTE: Need to test out hashBLK Return
    def downloadMissingBlocks(self, FileName, BlockServ, MissingBlocks):
        BlockServerHandler = BlockServ.ConnectAndReturnHandler()
        # This overwrites the data...deleting it.
        if not FileName in self.clientHandler.FileBlockList:
            self.clientHandler.FileBlockList[FileName] = {}

        for blk in MissingBlocks:
            hashBlk = BlockServerHandler.getBlock(blk)
            if hashBlk != None:
                self.clientHandler.FileBlockList[FileName][blk] = hashBlk
            else:
                return False
        BlockServ.CloseConnection()
        return True
        pass    

    # NOTE: Assumption is that Blocks are local and stored in clientHandler.FileBlockList
    #       And that the guide to build the file back up is in OrderedHashList.
    def combineBlocksToFile(self, FileName, OrderedHashList):
        hLIST = []
        for hash in OrderedHashList:  # change this.
            for key in self.clientHandler.FileBlockList:
                if hash in self.clientHandler.FileBlockList[key]:
                    hLIST.append(self.clientHandler.FileBlockList[key][hash].block)
                    break  # So to not copy more
        fd = open(self.clientHandler.FileDirectory + FileName, "wb")
        temp = "".join([str(x) for x in hLIST])
        fd.write(temp)
        fd.close()
        pass    