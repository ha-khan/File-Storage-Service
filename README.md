# Distributed File Storage Service.
This project is composed of three components: client program, block server, and a metadata server. All three components are located in the 
src folder a long with two other files needed. This project is essentially a Dropbox clone which currently works on a single host environment with IPC using the thrift RPC framework. The following link is an old version of how Dropbox works; and serves as the inspiration for the architecture. 

Dropbox protocol for blockfile transfer: https://blogs.dropbox.com/tech/2014/07/streaming-file-synchronization/

## Getting Started