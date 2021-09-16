docker stop $(docker ps -a -q)

docker start namingService
docker start rendezvousHashing0
docker start rendezvousNode0
docker start rendezvousNode1
docker start rendezvousNode2
docker start rendezvousNode3
docker start rendezvousNode4
docker start rendezvousNode5
docker start rendezvousHashing1