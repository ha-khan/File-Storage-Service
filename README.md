# Distributed File Storage Service
This project is composed of a client program, a blockfile server, and a metadata server. All three components are located in the 
src folder. This project is essentially a Dropbox clone which currently works on a single host environment with IPC using the thrift RPC framework. The following link serves as an inspiration for how the upload/download client works as well as the structure of both the blockfile server and metadata server.

https://blogs.dropbox.com/tech/2014/07/streaming-file-synchronization/

## Requirements

The project uses Python 2.7 and apache thrift is needed to compile the thrift files. 
The requirements.txt file contains the list of python modules that are needed to run 
the programs.

## Getting Started

### Directory Structure
    .
    ├── scripts                 # Start up shell scripts for the (client, blockfile server, metadata server)
    ├── src                     # location of (client, blockfile server, metadata server) code along with thrift code.
    ├── tests                   # Location of testing files. 
    ├── README.md
    ├── config.txt              # Configures the servers with their listening ports. 
    └── requirements.txt 

### Starting up Block/Metadata Server
Run the scripts in the document root of the project.
Note: Each script needs to run in its own terminal window.  
```
bash scripts/runBlockServer.sh config.txt             # Start the blockfile server on the port specified in the config.txt file
bash scripts/runMetaServer.sh config.txt 1            # Start the metadata server on the port specified in the config.txt and give it some ID.
```

A thing to note is that in the shell scripts; the path to the python scripts located in src folder will need to be changed 
according to your filesystem. 

#### Blockfile server start up
```
(filestorage) HAK:File-Storage-Service hamzakhan$ bash scripts/runBlockServer.sh config.txt 
Initializing block server
Starting server on port :  7080
```
#### Metadata server start up
```
(filestorage) HAK:File-Storage-Service hamzakhan$ bash scripts/runMetaServer.sh config.txt 1 
Initializing metadata server
Starting server on port :  10080
```
## Using the Client 
Now that both the Blockfile server and Metadata server are up, the client program 
can be used. 
```
bash scripts/runClient.sh <config_file> <base_dir> <command> <filename>         

<config_file>           # Exactly like the previous scripts. 

<base_dir>              # The directory path from which the files are uploaded from and download to. 

<command>               # One of the following commands: upload, download, delete. 

<filename>              # The file that the client program will operate on. 
```

#### Client successful upload
```
(filestorage) HAK:File-Storage-Service hamzakhan$ bash scripts/runClient.sh config.txt files upload DC-Computer_Test.pdf
OK
(filestorage) HAK:File-Storage-Service hamzakhan$ 
```

#### Client unsuccessful upload
```
(filestorage) HAK:File-Storage-Service hamzakhan$ bash scripts/runClient.sh config.txt files upload DC-ComputTest.pdf
ERROR
(filestorage) HAK:File-Storage-Service hamzakhan$ 
```

While the error message is not exactly the easiest to decipher, we essentially tried to upload a file that does not exist. 
Download and delete work the same way and will give an error message if download/delete is unsuccessful. 

## WARNING
Make sure to test upload/download with files that you have a lot of copies of. 
If you upload a file and then delete it from the directory and one of the 
servers crashes on your computer, then you will lose that file. I suggest 
testing it with the various files that I have set in the files directory. 
