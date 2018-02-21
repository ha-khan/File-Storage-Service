
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



# TritonTransfer Object file.
class TritonTransfer():

    def __init__(self, argumentList):
        self.CheckArgumentAmount(argumentList)
        self.ConfigurationFile = argumentList[1]
        self.FileDirectory = argumentList[2]
        self.__CheckDirectoryPath()
        self.OperationType = argumentList[3]
        # Will store a dict; of the form {File_Name->dict(Hash->hashBlock(type)}
        self.FileBlockList = {}
        # To save the order of the HASH for FileName; mainly for when files are processed in local dir.
        self.FileToHashList = {}
        pass

    def __CheckDirectoryPath(self):
        if self.FileDirectory[-1] != "/":
            self.FileDirectory = self.FileDirectory + "/"
        pass

    def CheckArgumentAmount(self, argumentList):
        if len(argumentList) < 5:
            print "Invocation : <executable> <config_file> <base_dir> <command> <filename>"
            exit(-1)
        pass

    # NOTE: Extendble to other HASH Functions.
    def BreakFileAndComputHash(self, hType, FName):
        if hType == "sha256":
            return self.__BreakFileHelper("sha256", FName)
        else:
            return None
            pass
        pass

    # NOTE: (string)fileList; List of file names in Directory.
    def storeLocalFiles(self, fileList):
        for file in fileList:
            self.FileBlockList[file] = self.__BreakFileHelper("sha256", file)
        pass

    # NOTE: Breaks a file into 4MB blocks and returns a HASH->hashBlock mapping for entire file.
    def __BreakFileHelper(self, hType, FileName):
        FPATH = self.FileDirectory + FileName
        FileDes = open(FPATH, "rb")
        HMAP = {}
        orderedHashList = []
        while True:
            block = FileDes.read(4194304)  # Change this to 4194304
            if block:
                temp = hashBlock()
                temp.hash = hashlib.sha256(block).hexdigest()
                orderedHashList.append(temp.hash)  # To preserve hash order.
                temp.block = block
                temp.status = "OK"
                HMAP[temp.hash] = temp
            else:
                self.FileToHashList[FileName] = orderedHashList
                return HMAP
                break
        # Ideally; Don't need this..
        self.FileToHashList[FileName] = orderedHashList
        return HMAP
        pass

    # NOTE: Uploads the blocks that are mising on the BlockServer.
    #      Also, BSS.storeBlock returns a response type. However, this
    #      Function doesn't return anything
    def UploadFileBlocks(self, FileName, MissingHashList, BSS):
        for hash in MissingHashList:
            temp = self.FileBlockList[FileName][hash]
            BSS.storeBlock(temp)
        pass

    # TODO: Port is returned as int.
    # change this to be more modular.
    def ParsePort(self, serverType, configFile):
        f = open(configFile)
        for l in f:
            if serverType in l:  # Implication that serverType is of type string....
                p1 = l.index(":") + 2
                p2 = (len(l))
                return int(l[p1:p2])
        pass

    # NOTE: (file)FileToSend ->  uploadResponse(resp)
    def UploadFile(self, FileToSend, MDS):
        resp = MDS.storeFile(FileToSend)
        return resp
        pass

    # NOTE: Should be an outside function.
    def OutputResponseToConsole(self, response):
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
        pass

    # TODO: (string)FileName -> file(temp)
    def GenerateFile(self, FileName):
        if FileName in self.FileBlockList:
            temp = file()
            temp.filename = FileName
            temp.status = responseType.OK
            temp.version = int(1)  # Versioning doesn't matter for Part 1.
            temp.hashList = self.FileToHashList[FileName]
            return temp
        else:
            temp = file()
            temp.status = responseType.ERROR
            return temp
        pass