#!/usr/bin/env python

import sys
import os

sys.path.append('gen-py')

from shared.ttypes import *
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

    singleton = UDC(sys.argv)

    file_name = sys.argv[4]

    operation_type = sys.argv[3]

    # Read all files in directory; and create a mapping of all available blocks.
    every_file = os.listdir(singleton.GetFileDirectory())

    # Store mapping of files in address space of client process. 
    singleton.storeLocalFiles(every_file)

    if operation_type == "upload":
        print "Upload"
        result = singleton.upload(file_name)
        OutputResponseToConsole(result)
    elif operation_type == "download":
        print "Download"
        result = singleton.download(file_name)
        OutputResponseToConsole(result)
    elif operation_type == "delete":
        print "Delete"
        singleton.delete(file_name)
    else:
        print "INPUT ERROR"

if(__name__ == "__main__"):
    main()
