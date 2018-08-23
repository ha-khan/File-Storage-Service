import unittest
from mock import MagicMock
from MetadataServer import MetadataServerHandler
from shared.ttypes import *


class TestMetadataServer(unittest.TestCase):

    def test_storeFile_Missing_Blocks(self):
        mss = MetadataServerHandler("/Users/hamzakhan/Desktop/CAREER/Projects/File-Storage-Service/config.txt", 1)
        mss._CheckForBlockList = MagicMock(return_value=[1, 2, 3])  # Non-Empty implies blocks missing, file not upload.
        mock_file = file()
        mock_file.filename = "Missing.txt"
        mock_file.hashList = [123]
        val = mss.storeFile(mock_file)
        #
        self.assertEqual(val.status, uploadResponseType.MISSING_BLOCKS)


    def test_storeFile_OK(self):
        mss = MetadataServerHandler("/Users/hamzakhan/Desktop/CAREER/Projects/File-Storage-Service/config.txt", 1)
        mss._CheckForBlockList = MagicMock(return_value=[])  # Empty implies no block missing, so file upload OK.
        mock_file = file()
        mock_file.filename = "Empty.txt"
        mock_file.hashList = [123]
        val = mss.storeFile(mock_file)
        #
        self.assertEqual(val.status, uploadResponseType.OK)

if __name__ == '__main__':
    unittest.main()

