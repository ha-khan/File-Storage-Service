# Distributed File Storage Service.
This project is composed of a client program, a block server, and a metadata server. All three components are located in the 
src folder. This project is essentially a Dropbox clone which currently works on a single host environment with IPC using the thrift RPC framework. The following link serves as an inspiration for how the upload/download client works as well as the structure of both the blockfile server and metadata server.

https://blogs.dropbox.com/tech/2014/07/streaming-file-synchronization/

## Getting Started

### Requirements

The project uses Python 2.7 and apache thrift is needed to compile the thrift files. 
The requirements.txt file contains the list of python modules that are needed to run 
the programs. This project is also composed of a virtualenv which will also be needed
in your python modules. 

### Starting the virtualenv
