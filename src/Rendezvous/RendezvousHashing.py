from src.Rendezvous.RendezvousNode import RendezvousNode
from src.Routing.router_abstract import AbstractRouterClass

import src.ServerInformation.ServerInformation_pb2 as SI_pb2
import src.ServerInformation.ServerInformation_pb2_grpc as SI_pb2_grpc

import src.Rendezvous.RendezvousHashing_pb2 as RH_pb2
import src.Rendezvous.RendezvousHashing_pb2_grpc as RH_pb2_grpc

import src.Rendezvous.RendezvousNode_pb2 as RN_pb2
import src.Rendezvous.RendezvousNode_pb2_grpc as RN_pb2_grpc

import grpc
import socket
import argparse
from concurrent import futures

# look how to import from AbstractRouterClass since it is our abstract class. Maybe like this: RendezvousHashing(AbstractRouterClass(RH_pb2_grpc.RendezvousHashingServicer))
# DONE: inheriting from two classes at the same time could be done by separating them with a comma
class RendezvousHashing(AbstractRouterClass, RH_pb2_grpc.RendezvousHashingServicer):
    def __init__(self) -> None:
        channel = grpc.insecure_channel("172.17.0.2:50050")
        self.server_information_stub = SI_pb2_grpc.ServerInformationStub(channel)
        ## TODO: Locking this attribute to ensure sync
        self._list_of_nodes = {}
        self.get_all_nodes()

    def get_all_nodes(self):
        """
        Updated the list of all available nodes from the ServerInformation
        """
        request = SI_pb2.GetAllRequest(type=SI_pb2.NODE)
        responses = self.server_information_stub.get_all_(request)
        for response in responses:
            self._list_of_nodes[response.name] = response.ip_address

    # TODO: if we use multiple routers, we need to ensure that all of them have the same _list_of_nodes, currently its gets only updated in the init.
    # DONE: update the ServerInformation, since its updated, when a new node launches
    def add_node(self, request, context):
        """
        adds a new Node into the Router.
        Also handles node balancing

        node: the node that should be added
        """
        print(self._list_of_nodes)
        self._list_of_nodes[request.name] = request.ip_address
        self.redistribute_objects_to_new_node(request.ip_address)
        return RH_pb2.RendezvousEmpty()

    def redistribute_objects_to_new_node(self, ip_address):
        """
        Redistributes all Key,Values of a all Nodes, if the new node is the champion

        node: the node that will be added
        """

        # TODO: threading?
        for _, n_ip in self._list_of_nodes.copy().items():
            if n_ip == ip_address:
                continue

            # TODO: catch if we cant connect to the node
            channel = grpc.insecure_channel(n_ip)
            node_stub = RN_pb2_grpc.RendezvousNodeStub(channel)
            request = RN_pb2.NodeSendItemToNewNodeRequest(ip_address=ip_address)
            # TODO: look into if this works
            node_stub.send_item_to_new_node(request)

    # TODO: update the ServerInformation
    # TODO: remove_node not working
    def remove_node(self, request, context):
        """
        removes a Node from the Router.
        Also handles node balancing

        node: the node that should be deleted
        """
        del self._list_of_nodes[request.name]
        self.redistribute_objects_from_deleted_node(request.ip_address)

    # TODO: it is not done, since it cant call the function on the node. Also the call was wrong
    # DONE: can we call the forward_to_responsible_node function if we dont use rpc?
    def redistribute_objects_from_deleted_node(self, ip_address):
        """
        Redistributes all Key,Values of a deleted Node

        node: the node that should be deleted
        """
        objects_on_node = {}
        channel = grpc.insecure_channel(node[0])
        node_stub = RN_pb2_grpc.RendezvousNodeStub(channel)
        responses = node_stub.get_objects()

        # reconstruct the dictionary of objects saved on the node
        for i, response in enumerate(responses):
            objects_on_node[response.key] = response.value

        # TODO: This solution is probably not efficient, but I'm not sure whether it's a design or programming issue. 
        for k, v in objects_on_node.items():
            self.forward_to_responsible_node(k, v)


    # DONE: the request gets forwarded directly from the router after finding the responsible node
    def forward_to_responsible_node(self, request, context):
        """
        finds the responsible node, for a given key

        key: the key of which we want to know the node

        return the Node for the given key
        """
        champion_ip = None
        champion_name = None
        maxValue = -1

        # TODO: threading
        for _, n_ip in self._list_of_nodes.copy().items():
            # note: a node tuple consists of an ip_address and name
            # connect to the node
            channel = grpc.insecure_channel(n_ip)
            node_stub = RN_pb2_grpc.RendezvousNodeStub(channel)

            # calc the hash score from the node
            request_node = RN_pb2.NodeHashValueForRequest(key=request.key)
            currentValue = node_stub.hash_value_for_key(request_node)

            # check if node is the biggest
            if currentValue.hashValue > maxValue:
                maxValue = currentValue.hashValue
                champion_ip = n_ip

        # creates a connection to the champion node
        channel = grpc.insecure_channel(champion_ip)
        node_stub = RN_pb2_grpc.RendezvousNodeStub(channel)

        # sends the request to the node
        request = RN_pb2.NodeGetRequest(type=request.type, key=request.key, value=request.value)
        responses = node_stub.get_request(request)

        for i in responses:
            pass

        return RH_pb2.RendezvousEmpty()

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
