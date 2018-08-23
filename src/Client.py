#!/usr/bin/env python

import sys
import os
import logging

sys.path.append('gen-py')

from shared.ttypes import *
from UDC import UDC

def OutputResponseToConsole(response):
    if response == uploadResponseType.MISSING_BLOCKS:
        logging.info("MISSING BLOCKS")
    elif response == uploadResponseType.FILE_ALREADY_PRESENT:
        logging.info("FILE ALREADY PRESENT")
    elif response == uploadResponseType.OK:
        logging.info("OK")
    elif response == uploadResponseType.ERROR:
        logging.info("ERROR")
    else:
        logging.info("UNKNOWN RESPONSE")


def main():

    logging.basicConfig(level=logging.INFO)
    logging.info("Starting Client")

    singleton = UDC(sys.argv)

    file_name = sys.argv[4]

    operation_type = sys.argv[3]

    # Read all files in directory; and create a mapping of all available blocks.
    every_file = os.listdir(singleton.GetFileDirectory())

    # Store mapping of files in address space of client process. 
    singleton.storeLocalFiles(every_file)

    if operation_type == "upload":
        logging.info("Uploading : " + file_name)
        result = singleton.upload(file_name)
        OutputResponseToConsole(result)
    elif operation_type == "download":
        logging.info("Downloading : " + file_name)
        result = singleton.download(file_name)
        OutputResponseToConsole(result)
    elif operation_type == "delete":
        logging.info("Deleting : " + file_name)
        singleton.delete(file_name)
    else:
        print "INPUT ERROR"

if(__name__ == "__main__"):
    main()
