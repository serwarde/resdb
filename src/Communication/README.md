# Quick Overview

|                  | gRPC           | Thrift         | RPyX        | XMLRPC |
|------------------|----------------|----------------|-------------|--------|
| Getting Started  | x              | -              | x           | x      |
| Documentation    | x              | -              | x           | x      |
| Language Support | C++, Python,.. | C++, Python,.. | Python only |  C++, Python,.. |
| Maintenance      | x              | x              | -           | -      |
| Streaming        | x              | x              | x           | x      |
| Can work w/o IDL  | -              | -              | x           | x      |

# gRPC

## Download

>pip install grpcio-tools

## Proto Format 

The format is really straight forward:
if you struggle, you can look at this [guide](https://developers.google.com/protocol-buffers/docs/overview)

## File creation:
After Creating the idl file (the file with .proto ending), you need to call:
>python -m grpc_tools.protoc --python_out=. --grpc_python_out=. --proto_path=. file_name.proto
to create two files which are needed for the server and client

## Start Server in docker:

to start the Server in Docker use the [deploy_container.sh](deploy_container.sh). If you are on windows you can just call each Command seperate. Don't forget to install docker first ;). 

## Pros:

- Multiple Language Support for both servers and clients.
- It uses HTTP/2 by default for connections.
- Abundant documentation.
- This project is actively supported by Google and others.
## Cons:

- Less flexibility (especially compared to rpyc).

# Apache Thrift 

## Download 
>https://thrift.apache.org/download

and

>pip install thrift

## create files

>thrift-0.14.1.exe -r --gen py tutorial.thrift 

>thrift-0.14.1.exe -r --gen py shared.thrift

## Pros:

- Thrift supports container types list, set and map. They also support constants. This is not supported by Protocol Buffers. However, rpyc supports all python and python library types - you can even send a numpy array in an RPC call. (Edit: proto3 supports those types too. Thanks Barak Michener for pointing this out.)

## Cons:

- Python doesn’t feel like a primary language for Thrift. Having to add sys.path.append('gen-py') doesn’t make for a smooth python experience.
- Documentation and online discussions seem relatively scarce compared to gRPC.

# RPyC

## download

> pip install rpyc

## Pros:

- Probably the easiest to get started. No need to understand Protocol Buffers or Thrift syntax.
- Extremely flexible. No need to formally use IDL (Interface Definition Language) to define the client-server interfaces. Simply start implementing your code - it embraces python’s Duck Typing.

## Cons:

- Lack of multiple client languages.
- Lack of formally defined service interface can potentially cause maintenance issues if the codebase becomes large enough.

# XMLRPC

## Download

nothing

## Pros:

- Easy and straight forward

## Cons:

- didnt look into it

# xmlrpc vs thrift

## Difference

XML-RPC is XML based, this it is by nature more verbose, leading to larger messages and mopre traffic. In addition, XML must be parsed, while Thrift's binary format is quite effective, with regard to both size and processing speed.

## Which one is speed

One of Apache Thrift's main goals is efficiency (read: speed)

## Which one is ease to use

With Apache Thrift, you get a single package which contains compiler and runtime libraries for approx. 20 languages, covering Windows, Linux and Apple platforms. In contrast, XML-RPC (as well as SOAP) relies on what you get with your IDE and/or what is available as 3rd-party components, including any incompatibilities that may or may not be cause by that