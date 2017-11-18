# Distributed File Storage Service
This project is composed of a client program, a block server, and a metadata server. All three components are located in the 
src folder. This project is essentially a Dropbox clone which currently works on a single host environment with IPC using the thrift RPC framework. The following link serves as an inspiration for how the upload/download client works as well as the structure of both the blockfile server and metadata server.

https://blogs.dropbox.com/tech/2014/07/streaming-file-synchronization/

## Getting Started

### Directory Structure
    .
    ├── files                   # Folder where files are uploaded/downloaded.
    ├── filestorage             # Virtualenv for this project.
    ├── gen-py                  # Generated from thrift compiler.
    ├── scripts                 # Start up shell scripts for the (client, block server, metadata server)
    ├── src                     # location of (client, block server, metadata server) code along with thrift code.
    ├── tests                   # Location of testing files. 
    ├── README.md
    ├── config.txt
    └── requirements.txt 

### Requirements

The project uses Python 2.7 and apache thrift is needed to compile the thrift files. 
The requirements.txt file contains the list of python modules that are needed to run 
the programs. This project is also composed of a virtualenv which will also be needed
in your python modules. The pip package manager is also used 

### Starting the virtualenv
```
source filestorage/bin/activate
pip list
```
Running pip list will show all of the modules in this virtualenv, which will be 
isolated from your global modules. Mine shows the following. 
```
pip (9.0.1)
setuptools (36.7.2)
six (1.11.0)
thrift (0.10.0)
wheel (0.30.0)
 ```

### Starting up Block/Metadata Server
