# TODO:

- test with multiple nodes
- write bash skript to create multiple nodes
- write test class for the nodes
- write test class for the Routers
- write test class for the load balancer

# ServerInformation

The Serverinformation class is used to store the name and ip:port of the Load_balancers, Routers and Nodes. It is currently a SPoF. We use it currently to skip the synchronization of the Servers. Since all servers call this nde if they want to call other Servers. 

Later this Server may be deleted or just be used as a backup mechanism if all Servers from a specifc kind (Node, LB, Router) fail.

# Load Balancer

The Load Balancer is used to balance the load to diffrent routers. Currently it does not save the routers locally. It gets the routers from the ServerInformationServer. Later the routers should be saved locally to be robust against a SPoF. 

## request function

The request function gets a request from the user. inside the function a random router is returned from the ServerInformationServer. This router is then called to find the resposible node for a given key. The ip_address is the returend and after that called from the load_balancer to do the request inside the node.

We want to change that the design so that the router does this instead.

## Additional thoughts

The LoadBalancer is currently not a GRPC Server. But it may should be one, else a client cant send a request to the server.

# RendezvousHashing

The RendezvousHashing or Router is used as a middleman between the load_balancer and node. The router should know all nodes (currently gets them from ServerInformationServer). The router is also resposible to redistribute keys if a node gets added or deleted. And forwards the load_balancer request to the correct node.

## find_responsible_node function

This fuction loops over all nodes and calculates the hashscore for the specifc key inside the node. It then return the name and ip of this node. Same as before we want to change it, so that we directly call the new node.

# RendezvousNode

The Node is used to store the key, value pairs. The rendezvous node uses and additional weight parameter. It is used to make the node more likely to be choosen. It can be used for example if the node has more Space or a higher computation power.

## get_request

This fuction is used to add, delete, update or get the value for a specific key. Currently it does not return anything. This is problematic for the get function.

## hash_value_for_key

This fuction is the core part of the Node. It calculates the hash value for a given key, seed and weight. 

## additional thought

Show we save the hash value for a key, would it be faster? how much space does it take?