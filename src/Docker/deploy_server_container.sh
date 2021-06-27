#!/bin/bash

# start script in src/docker
cd ../../

# start ServerInformation
docker build -t serverinformation -f src/Docker/Dockerfile_ServerInformation .
docker run -d -it --name serverInformation -p 50050:50050 serverinformation:latest

# starts a router
docker build -t rendezvoushashing -f src/Docker/Dockerfile_RenzRouter .
docker run -d -it --name rendezvousHashing0 -p 50150:50150 rendezvoushashing:latest

# starts a client
docker build -t rendezvousnode -f src/Docker/Dockerfile_RenzNode .
docker run -d -it --name rendezvousNode0 -p 50250:50250 rendezvousnode:latest
