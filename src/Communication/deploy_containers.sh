#!/bin/bash

docker build -t grpc_server -f Dockerfile_server .
docker build -t grpc_client -f Dockerfile_client .

docker run -d -it --name server -p 50051:50051 grpc_server:latest
docker run -d -it --name client grpc_client:latest
