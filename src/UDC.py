import sys
import os
import hashlib

sys.path.append('gen-py')


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

# Legacy Code.
from TritonTransfer import TritonTransfer

# Class definition file, which will abstract the file upload, download, and delete functions and make it easier for
# a client file to use. Currently acts as a wrapper for TritonTransfer; which is the legacy code that
# was used to help the Client file upload, download, and delete files.
# TODO: Add more to this. 
#
class UDC():

    # Input: List<string>(argumentList)
    # Return: None
    def __init__(self, argumentList):
        self.__clientHandler = TritonTransfer(argumentList)  # change this to argumentList
        self.__blockPort = self.__parsePort("block","config.txt") # TODO: Need to add passed in path to config..
        self.__metaDataPort = self.__parsePort("metadata1","config.txt")
        self.__BlockServerServiceState = BSS(self.__blockPort)
        self.__MetadataServerServiceState = MDD(self.__metaDataPort)

    # NOTE: This will populate the Dictionary in TritonTransfer, which stores a
    #       local listing of all the files in the directory including their corresponding Hash->blocks.
    # Input: List<string>(fileList)
    # Return: None
    def storeLocalFiles(self, fileList):
        self.__clientHandler.storeLocalFiles(fileList)

    # Input: string(serverType), string(configFile)
    # Return: int(port corresponding to this server {metadata, blockfile})
    def __parsePort(self, serverType, configFile):
        return self.__clientHandler.ParsePort(serverType, configFile)

    # Input: None
    # Return: string(res) 
    def GetFileDirectory(self):
        res = self.__clientHandler.getFileDirectory()
        return res

    # Input: BSS(BlockServerServiceState), string(FileName), List<string>(HashList), file(FileToSend), MDD(MetadataServerServiceHandler)
    # Return: responseType(secondResponse.status) 
    def __uploadFileAndBlocks(self, BlockServerServiceState, FileName, HashList, FileToSend, MetadataServerServiceHandler):
        BlockServerServiceHandler = BlockServerServiceState.ConnectAndReturnHandler()
        self.__clientHandler.UploadFileBlocks(
            FileName, HashList, BlockServerServiceHandler)
        BlockServerServiceState.CloseConnection()
        secondResponse = self.__clientHandler.UploadFile(
            FileToSend, MetadataServerServiceHandler)
        return secondResponse.status

    # Input: string(FileName)
    # Return: file()
    def __generateFile(self, FileName):
        return self.__clientHandler.GenerateFile(FileName)

    # Input: file(FileToSend), MDD(MDS)
    # Return: response()
    def __uploadFile(self, FileToSend, MDS):
        return self.__clientHandler.UploadFile(FileToSend, MDS)

    # Input: MDD(MetadataServerServiceHandler), string(FileName)
    # Return: List<string>
    def __findMissingBlocks(self, MetadataServerServiceHandler, FileName):
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
            for key in self.__clientHandler.FileBlockList:
                if hash in self.__clientHandler.FileBlockList[key]:
                    Flag = True
            if not Flag:
                MissingBlocks.append(hash)
            Flag = False  # For next round.
        return MissingBlocks

    # Input: string(FileName), BSS(BlockServ), List<string>(MissingBlocks)
    # Return: bool - Always returns True, modify later.
    def __downloadMissingBlocks(self, FileName, BlockServ, MissingBlocks):
        BlockServerHandler = BlockServ.ConnectAndReturnHandler()
        # This overwrites the data...deleting it.
        if not FileName in self.__clientHandler.FileBlockList:
            self.__clientHandler.FileBlockList[FileName] = {}

        for blk in MissingBlocks:
            hashBlk = BlockServerHandler.getBlock(blk)
            if hashBlk != None:
                self.__clientHandler.FileBlockList[FileName][blk] = hashBlk
            else:
                return False
        BlockServ.CloseConnection()
        return True

    # NOTE: Assumption is that Blocks are local and stored in __clientHandler.FileBlockList
    #       And that the guide to build the file back up is in OrderedHashList.
    # Input: string(FileName), List<string>(Hash_Signature)
    # Return: None.
    def __combineBlocksToFile(self, FileName, OrderedHashList):
        hLIST = []
        for hash in OrderedHashList:  
            for key in self.__clientHandler.FileBlockList:
                if hash in self.__clientHandler.FileBlockList[key]:
                    hLIST.append(
                        self.__clientHandler.FileBlockList[key][hash].block)
                    break  # So to not copy more
        fd = open(self.__clientHandler.FileDirectory + FileName, "wb")
        temp = "".join([str(x) for x in hLIST])
        fd.write(temp)
        fd.close()

    def upload(self, FileName):
        FileToSend = self.__generateFile(FileName)
        MetadataServerServiceHandler = self.__MetadataServerServiceState.ConnectAndReturnHandler()
        if FileToSend.status == responseType.OK:
            response = self.__uploadFile(FileToSend, MetadataServerServiceHandler)
            if response.status == uploadResponseType.MISSING_BLOCKS:
                return self.__uploadFileAndBlocks(self.__BlockServerServiceState, FileName, response.hashList, FileToSend, MetadataServerServiceHandler)
            else:
                return response.status
        else:
            return responseType.ERROR

    def download(self, FileName):
        MetadataServerServiceHandler = self.__MetadataServerServiceState.ConnectAndReturnHandler()
        FileData = MetadataServerServiceHandler.getFile(FileName)
        OrderedHashList = FileData.hashList
        MissingBlocks = self.__findMissingBlocks(MetadataServerServiceHandler, FileName)
        if MissingBlocks != None:
            if self.__downloadMissingBlocks(FileName, self.__BlockServerServiceState, MissingBlocks):
                self.__combineBlocksToFile(FileName, OrderedHashList)
                return responseType.OK
            else:
                return responseType.ERROR 
        else:
            return responseType.ERROR

    def delete(self, FileName):
        fileDel = self.__generateFile(FileName)
        MetadataServerServiceHandler = self.__MetadataServerServiceState.ConnectAndReturnHandler() 
        response =  MetadataServerServiceHandler.deleteFile(fileDel)
        return response.message