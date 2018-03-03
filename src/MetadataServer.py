#!/usr/bin/env python

import sys
sys.path.append('gen-py')

# Thrift specific imports
from thrift import Thrift
from thrift.transport import TSocket
from thrift.server import TServer
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

# Protocol specific imports
from metadataServer import MetadataServerService
from metadataServer.ttypes import *
from shared.ttypes import *
from blockServer.ttypes import *
from blockServer import BlockServerService

# Bindings to communicate with Blockfile server.
from BSS import BSS



# Review the files in the thrift folder titled metadataServer.thrift and shared.thrift. 
#
# This file contains the implementation code for the Metadata Server, which essentially keeps track
# of a dictionary that contains (file name) -> {h1, h2, h3, ..., hn}, where each h1 ... hn is a hashed
# signature of a block that is contained in the original file. 
#
class MetadataServerHandler():

    # Input: string(config_path), string(my_id) 
    # Return: None
    def __init__(self, config_path, my_id):
        self.config_path = config_path
        self.my_id = my_id
        self.FileHashList = {}  # HashMap of  FileName : Ordered list of hash that compose file.
        pass
    
    # Input: string(filename)
    # Return: file(temp)
    def getFile(self, filename):
        if filename in self.FileHashList:
            temp = file()
            temp.filename = filename
            temp.hashList = self.FileHashList[filename]
            temp.status = responseType.OK
            return temp
        else:
            temp = file()
            temp.status = responseType.ERROR
            return temp
        pass

    # Input: file(file)  
    # Return: uploadResponse(resp)
    def storeFile(self, file):
        MissingList = self.__CheckForBlockList(file.hashList)
        if len(MissingList) != 0:
            resp = uploadResponse()
            resp.hashList = MissingList
            resp.status = uploadResponseType.MISSING_BLOCKS
        else:
            self.FileHashList[file.filename] = file.hashList
            resp = uploadResponse()
            resp.hashList = MissingList
            resp.status = uploadResponseType.OK
        return resp
        pass

    # Input: file(fileDel)
    # Return: response(resp)
    def deleteFile(self, fileDel):
        filename = fileDel.filename
        if filename in self.FileHashList:
            del self.FileHashList[filename]
            resp = response()
            resp.message = responseType.OK
            return resp
        else:
            resp = response()
            resp.message = responseType.ERROR
            return resp
        pass

    # Input: string(serverName)
    # Return: int(l[p1:p2])
    def readServerPort(self, serverName):
        f = open(self.config_path)
        for l in f:
            if serverName in l:
                p1 = l.index(":") + 2
                p2 = (len(l))
                return int(l[p1:p2])
        pass

    # Input: list<string>(HashList) 
    # Return: list<string>(MissingBlocks)
    def __CheckForBlockList(self, HashList):
        # Search for port of block server from config.txt
        port = self.readServerPort("block")
        bService = BSS(port)
        BlockConnect = bService.ConnectAndReturnHandler()
        MissingBlocks = []
        temp = hashBlock()
        for hash in HashList:
            temp.hash = hash
            response = BlockConnect.hasBlock(temp.hash)
            if (not response):
                MissingBlocks.append(temp.hash)
        # print MissingBlocks
        bService.CloseConnection()
        return MissingBlocks
        pass


# TODO: Add Try~Catch
def main():
    if len(sys.argv) < 3:
        print "Invocation <config_file> <id>"
        exit(-1)

    config_path = sys.argv[1]

    my_id = sys.argv[2]

    print "Initializing metadata server"

    handler = MetadataServerHandler(config_path, my_id)

    ThisServerNum = "metadata" + my_id

    port = handler.readServerPort(ThisServerNum)

    # Define parameters for thrift server
    processor = MetadataServerService.Processor(handler)
    transport = TSocket.TServerSocket(port=port)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    # Create a server object
    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
    print "Starting server on port : ", port

    server.serve()


if(__name__ == "__main__"):
    main()
