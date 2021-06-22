#!/bin/bash

cd ../../

# start ServerInformation
docker build -t serverinformation -f src/Docker/Dockerfile_ServerInformation .
docker run -d -it --name serverInformation -p 50052:50052 serverinformation:latest
