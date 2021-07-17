from src.Rendezvous.RendezvousNode import RendezvousNode
from src.Routing.router_abstract import AbstractRouterClass

import src.ServerInformation.ServerInformation_pb2 as SI_pb2
import src.ServerInformation.ServerInformation_pb2_grpc as SI_pb2_grpc

import src.Rendezvous.RendezvousHashing_pb2 as RH_pb2
import src.Rendezvous.RendezvousHashing_pb2_grpc as RH_pb2_grpc

import src.Rendezvous.RendezvousNode_pb2 as RN_pb2
import src.Rendezvous.RendezvousNode_pb2_grpc as RN_pb2_grpc

import src.Rendezvous.type_pb2 as type_pb2

from collections import defaultdict
import grpc
import socket
import argparse
from concurrent import futures

# look how to import from AbstractRouterClass since it is our abstract class. Maybe like this: RendezvousHashing(AbstractRouterClass(RH_pb2_grpc.RendezvousHashingServicer))
# DONE: inheriting from two classes at the same time could be done by separating them with a comma (nice one!)
class RendezvousHashing(AbstractRouterClass, RH_pb2_grpc.RendezvousHashingServicer):
    def __init__(self) -> None:
        channel = grpc.insecure_channel("172.17.0.2:50050")
        self.server_information_stub = SI_pb2_grpc.ServerInformationStub(channel)
        ## TODO: Locking this attribute to ensure sync
        self._dict_nodes = {}
        self.get_all_nodes()

    def get_all_nodes(self):
        """
        Updated the list of all available nodes from the ServerInformation
        """
        request = SI_pb2.GetAllRequest(type=SI_pb2.NODE)
        responses = self.server_information_stub.get_all_(request)
        for response in responses:
            self._dict_nodes[response.name] = response.ip_address

    # TODO: if we use multiple routers, we need to ensure that all of them have the same _dict_nodes, currently its gets only updated in the init.
    # TODO: Serverinfomration send an update when a node gets added or delted
    # DONE: update the ServerInformation, since its updated, when a new node launches
    # TODO: rethink done above. We maybe should just do it in the add_node
    # TODO: add paramerter so we can use this function to update the information in all nodes
    def add_node(self, request, context):
        """
        adds a new Node into the Router.
        Also handles node balancing

        node: the node that should be added
        """
        print(self._dict_nodes)
        self._dict_nodes[request.name] = request.ip_address
        self.redistribute_objects_to_new_node(request.ip_address)
        return RH_pb2.RendezvousEmpty()

    def redistribute_objects_to_new_node(self, ip_address):
        """
        Redistributes all Key,Values of a all Nodes, if the new node is the champion

        node: the node that will be added
        """

        # TODO: threading?
        for _, n_ip in self._dict_nodes.copy().items():
            if n_ip == ip_address:
                continue

            # TODO: catch if we cant connect to the node
            channel = grpc.insecure_channel(n_ip)
            node_stub = RN_pb2_grpc.RendezvousNodeStub(channel)
            request = RN_pb2.NodeSendItemToNewNodeRequest(ip_address=ip_address)
            node_stub.send_item_to_new_node(request)

    # DONE: update the ServerInformation
    # TODO: remove_node not working
    def remove_node(self, request, context):
        """
        removes a Node from the Router.
        Also handles node balancing

        node: the node that should be deleted
        """
        request = SI_pb2.DeleteRequest(type=SI_pb2.NODE, name=request.name)
        self.stub.delete_(request)

        del self._dict_nodes[request.name]
        
        self.redistribute_objects_from_deleted_node(request.ip_address)

    # TODO: it is not done, since it cant call the function on the node. Also the call was wrong
    # DONE: can we call the forward_to_responsible_node function if we dont use rpc?
    def redistribute_objects_from_deleted_node(self, ip_address):
        """
        Redistributes all Key,Values of a deleted Node

        node: the node that should be deleted
        """
        objects_on_node = defaultdict(list)
        channel = grpc.insecure_channel(ip_address)
        node_stub = RN_pb2_grpc.RendezvousNodeStub(channel)
        responses = node_stub.get_objects()

        # reconstruct the dictionary of objects saved on the node
        for response in responses:
            objects_on_node[response.key].append(response.value)

        # TODO: This solution is probably not efficient, but I'm not sure whether it's a design or programming issue. 
        for key, vs in objects_on_node.items():
            champion_ip = self.find_responsible_node(key, self._dict_nodes.copy().items())
            
            channel = grpc.insecure_channel(champion_ip)
            node_stub = RN_pb2_grpc.RendezvousNodeStub(channel)

            for v in vs:
                request = RN_pb2.NodeGetRequest(type=type_pb2.ADD,key=key,value=v)
                responses = node_stub.get_request(request)

                for _ in responses:
                    pass

        objects_on_node.clear()


    # DONE: the request gets forwarded directly from the router after finding the responsible node
    def forward_to_responsible_node(self, request, context):
        """
        finds the responsible node, for a given key
        and sende the the request to the node.

        key: the key of which we want to know the node

        return the Node for the given key
        """

        champion_ip = self.find_responsible_node(request.key, self._dict_nodes.copy().items())

        # creates a connection to the champion node
        channel = grpc.insecure_channel(champion_ip)
        node_stub = RN_pb2_grpc.RendezvousNodeStub(channel)

        # sends the request to the node
        request = RN_pb2.NodeGetRequest(type=request.type, key=request.key, value=request.value)
        responses = node_stub.get_request(request)

        for i in responses:
            pass

        return RH_pb2.RendezvousEmpty()

    def find_responsible_node(self, key, dict_nodes_items):
        champion_ip = None
        maxValue = -1

        # TODO: threading
        for _, n_ip in dict_nodes_items:
            # note: a node tuple consists of an ip_address and name
            # connect to the node
            channel = grpc.insecure_channel(n_ip)
            node_stub = RN_pb2_grpc.RendezvousNodeStub(channel)

            # calc the hash score from the node
            request_node = RN_pb2.NodeHashValueForRequest(key=key)
            currentValue = node_stub.hash_value_for_key(request_node)

            # check if node is the biggest
            if currentValue.hashValue > maxValue:
                maxValue = currentValue.hashValue
                champion_ip = n_ip
        
        return champion_ip 

def serve(name, ip_address, port):
    # connects to the server information and registers itself
    channel = grpc.insecure_channel("172.17.0.2:50050")
    server_information_stub = SI_pb2_grpc.ServerInformationStub(channel)

    request = SI_pb2.AddRequest(
        type=SI_pb2.ROUTER, name=name, ip_address=f"{ip_address}:{port}"
    )
    _ = server_information_stub.add_(request)

    # starts the grpc server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    RH_pb2_grpc.add_RendezvousHashingServicer_to_server(RendezvousHashing(), server)
    server.add_insecure_port(f"{ip_address}:{port}")
    server.start()
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    # arguments
    parser = argparse.ArgumentParser(description='Create Rendezvous Router.')
    parser.add_argument('--name', '-n', type=str, help='The name of the Router', default="router1")
    parser.add_argument('--port', '-p', type=int, help='The port of the Router', default=50151)
    args = parser.parse_args()
    
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    
    print(f"starting Router '{args.name}': {ip_address}:{args.port}.")
    serve(args.name, ip_address, args.port)
