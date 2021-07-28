#!/bin/bash

# start script in src/docker
cd ../../

# allocates ports
net stop winnat
netsh int ipv4 add excludedportrange protocol=tcp startport=50050 numberofports=1
netsh int ipv4 add excludedportrange protocol=tcp startport=50151 numberofports=1
netsh int ipv4 add excludedportrange protocol=tcp startport=50251 numberofports=1
netsh int ipv4 add excludedportrange protocol=tcp startport=50252 numberofports=1
netsh int ipv4 add excludedportrange protocol=tcp startport=50253 numberofports=1
net start winnat

# deletes base image
docker rmi rendezvousbase

# deletes the NamingService
printf '%.s-' {1..100}
printf " deletes NamingService Server "
printf '%.s-' {1..100}; echo "" 
docker stop namingService
docker rm namingService
docker rmi namingservice

# deletes a router
printf '%.s-' {1..100}
printf " deletes Router Server "
printf '%.s-' {1..100}; echo ""
docker stop rendezvousHashing0
docker rm rendezvousHashing0
docker rmi rendezvoushashing0
docker stop rendezvousHashing1
docker rm rendezvousHashing1
docker rmi rendezvoushashing1

# deletes a nodes
printf '%.s-' {1..100}
printf " deltes Node Servers "
printf '%.s-' {1..100}; echo ""
docker stop rendezvousNode0 rendezvousNode1 rendezvousNode2 
docker rm rendezvousNode0 rendezvousNode1 rendezvousNode2
docker rmi rendezvousnode0 rendezvousnode1 rendezvousnode2

# build a base image
docker build -t rendezvousbase -f src/Docker/Dockerfile .

#starts the namingservice
printf '%.s-' {1..100}
printf " creates and starts NamingService Server "
printf '%.s-' {1..100}; echo ""
docker build -t namingservice -f src/Docker/Dockerfile_NamingService --build-arg PORT=50050 .
docker run -d -it --name namingService -p 50050:50050 namingservice:latest 50050

# starts a router
printf '%.s-' {1..100}
printf " creates and starts Router Server "
printf '%.s-' {1..100}; echo ""
docker build -t rendezvoushashing0 -f src/Docker/Dockerfile_RenzRouter --build-arg PORT=50151 .
docker run -d -it --name rendezvousHashing0 -p 50151:50151 rendezvoushashing0:latest 50151

# starts a node
printf '%.s-' {1..100}
printf " creates and starts Node Servers "
printf '%.s-' {1..100}; echo ""
docker build -t rendezvousnode0 -f src/Docker/Dockerfile_RenzNode --build-arg PORT=50251 .
docker build -t rendezvousnode1 -f src/Docker/Dockerfile_RenzNode --build-arg PORT=50252 .
docker build -t rendezvousnode2 -f src/Docker/Dockerfile_RenzNode --build-arg PORT=50253 .
docker run -d -it --name rendezvousNode0 -p 50251:50251 rendezvousnode0:latest 50251 1.0
docker run -d -it --name rendezvousNode1 -p 50252:50252 rendezvousnode1:latest 50252 1.0
docker run -d -it --name rendezvousNode2 -p 50253:50253 rendezvousnode2:latest 50253 1.1

# starts a second router
printf '%.s-' {1..100}
printf " creates and starts a second Router Server "
printf '%.s-' {1..100}; echo ""
docker build -t rendezvoushashing1 -f src/Docker/Dockerfile_RenzRouter --build-arg PORT=50152 .
docker run -d -it --name rendezvousHashing1 -p 50152:50152 rendezvoushashing1:latest 50152

printf '%.s-' {1..100}
printf " done "
printf '%.s-' {1..100}; echo ""