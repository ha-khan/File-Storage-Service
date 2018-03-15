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

# Class definition file, which will abstract the file upload, download, and delete functions and make it easier for
# a client file to use. Currently acts as a wrapper for TritonTransfer; which is the legacy code that
# was used to help the Client file upload, download, and delete files.
#
#


class UDC():

    # Input: List<string>(argumentList)
    # Return: None
    def __init__(self, argumentList):
        self.clientHandler = TritonTransfer(sys.argv)  # change this to argumentList
        self.__blockPort = self.parsePort("block","config.txt")
        self.__metaDataPort = self.parsePort("metadata1","config.txt")
        self.__BlockServerServiceState = BSS(self.__blockPort)
        self.__MetadataServerServiceState = MDD(self.__metaDataPort)

    # Input: List<string>(fileList)
    # Return: None
    # NOTE: That this will populate the Dictionary in TritonTransfer, which stores a
    # local listing of all the files in the directory including their corresponding Hash->blocks..
    def storeLocalFiles(self, fileList):
        self.clientHandler.storeLocalFiles(fileList)

    # Input: string(serverType), string(configFile)
    # Return: int(port corresponding to this server {metadata, blockfile})
    def parsePort(self, serverType, configFile):
        return self.clientHandler.ParsePort(serverType, configFile)

    # Input: BSS(BlockServerServiceState), string(FileName), List<string>(HashList), file(FileToSend), MDD(MetadataServerServiceHandler)
    # Return: Outputs to console the status of the response code..
    # TODO: Change this to a return.
    def uploadFileAndBlocks(self, BlockServerServiceState, FileName, HashList, FileToSend, MetadataServerServiceHandler):
        BlockServerServiceHandler = BlockServerServiceState.ConnectAndReturnHandler()
        self.clientHandler.UploadFileBlocks(
            FileName, HashList, BlockServerServiceHandler)
        BlockServerServiceState.CloseConnection()
        secondResponse = self.clientHandler.UploadFile(
            FileToSend, MetadataServerServiceHandler)
        return secondResponse.status

    # Input: string(FileName)
    # Return: file()
    def generateFile(self, FileName):
        return self.clientHandler.GenerateFile(FileName)

    # Input: file(FileToSend), MDD(MDS)
    # Return: response()
    def uploadFile(self, FileToSend, MDS):
        return self.clientHandler.UploadFile(FileToSend, MDS)

    # # Input: response(response)
    # # Return: Outputs to console, which needs to be changed.
    # def output(self, response):
    #     self.clientHandler.OutputResponseToConsole(response)

    # Input:
    # Return:
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

    # NOTE: Returns a list of blocks that are NOT locally stored in cHandler.
    # Input: List<string>
    # Return: List<string>
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

    # Input: string(FileName), BSS(BlockServ), List<string>(MissingBlocks)
    # Return: bool - Always returns True, modify later.
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

    # NOTE: Assumption is that Blocks are local and stored in clientHandler.FileBlockList
    #       And that the guide to build the file back up is in OrderedHashList.
    # Input: string(FileName), List<string>(Hash_Signature)
    # Return: None.
    def combineBlocksToFile(self, FileName, OrderedHashList):
        hLIST = []
        for hash in OrderedHashList:  
            for key in self.clientHandler.FileBlockList:
                if hash in self.clientHandler.FileBlockList[key]:
                    hLIST.append(
                        self.clientHandler.FileBlockList[key][hash].block)
                    break  # So to not copy more
        fd = open(self.clientHandler.FileDirectory + FileName, "wb")
        temp = "".join([str(x) for x in hLIST])
        fd.write(temp)
        fd.close()

    def upload(self, FileName):
        FileToSend = self.generateFile(FileName)
        MetadataServerServiceHandler = self.__MetadataServerServiceState.ConnectAndReturnHandler()
        if FileToSend.status == responseType.OK:
            response = self.uploadFile(FileToSend, MetadataServerServiceHandler)
            if response.status == uploadResponseType.MISSING_BLOCKS:
                return self.uploadFileAndBlocks(self.__BlockServerServiceState, FileName, response.hashList, FileToSend, MetadataServerServiceHandler)
            else:
                return response.status
        else:
            return responseType.ERROR

    def download(self, FileName):
        MetadataServerServiceHandler = self.__MetadataServerServiceState.ConnectAndReturnHandler()
        FileData = MetadataServerServiceHandler.getFile(FileName)
        OrderedHashList = FileData.hashList
        MissingBlocks = self.findMissingBlocks(MetadataServerServiceHandler, FileName)
        if MissingBlocks != None:
            if self.downloadMissingBlocks(FileName, self.__BlockServerServiceState, MissingBlocks):
                self.combineBlocksToFile(FileName, OrderedHashList)
                return responseType.OK
            else:
                return responseType.ERROR 
        else:
            return responseType.ERROR

    def delete(self, FileName):
        fileDel = self.generateFile(FileName)
        MetadataServerServiceHandler = self.__MetadataServerServiceState.ConnectAndReturnHandler() 
        response =  MetadataServerServiceHandler.deleteFile(fileDel)
        return response.message