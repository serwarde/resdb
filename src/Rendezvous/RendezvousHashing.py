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

    # DONE: save the nodes locally
    def get_all_nodes(self):
        """
        Updated the list of all available nodes from the ServerInformation
        """
        request = SI_pb2.GetAllRequest(type=SI_pb2.NODE)
        responses = self.server_information_stub.get_all_(request)
        for response in responses:
            self._list_of_nodes[response.ip_address] = response.name

    # TODO: update the ServerInformation
    # Done: add_node, remove_node are currently not working. they need to be callable by grpc.
    # Done: redistribute_objects_from_deleted_node, redistribute_objects_to_new_node should use grpc to call the nodes
    def add_node(self, node):
        """
        adds a new Node into the Router.
        Also handles node balancing

        node: the node that should be added
        """
        self._list_of_nodes[node.ip_address] = node.name
        self.redistribute_objects_to_new_node(node.ip_address, node.name)

    def remove_node(self, node):
        """
        removes a Node from the Router.
        Also handles node balancing

        node: the node that should be deleted
        """
        del self._list_of_nodes[node.ip_address]
        self.redistribute_objects_from_deleted_node(node.ip_address, node.name)

    def redistribute_objects_to_new_node(self, ip_address, name):
        """
        Redistributes all Key,Values of a all Nodes, if the new node is the champion

        node: the node that will be added
        """
        temp_list_of_nodes = self._list_of_node
        del temp_list_of_nodes[ip_address]

        # TODO: threading?
        for n_ip, n_name in temp_list_of_nodes.items():
            channel = grpc.insecure_channel(n_ip)
            node_stub = RN_pb2_grpc.RendezvousNodeStub(channel)
            node_stub.send_item_to_new_node(ip_address, name)

    # DONE: can we call the find_responsible_node function if we dont use rpc?
    def redistribute_objects_from_deleted_node(self, ip_address, name):
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
            self.find_responsible_node(k, v)


    # DONE: the request gets forwarded directly from the router after finding the responsible node
    def find_responsible_node(self, request, context):
        """
        finds the responsible node, for a given key

        key: the key of which we want to know the node

        return the Node for the given key
        """
        champion_ip = None
        champion_name = None
        maxValue = -1

        # TODO: threading
        for node in self._list_of_nodes:
            # note: a node tuple consists of an ip_address and name
            # connect to the node
            channel = grpc.insecure_channel(node[0])
            node_stub = RN_pb2_grpc.RendezvousNodeStub(channel)

            # calc the hash score from the node
            request_node = RN_pb2.NodeHashValueForRequest(request.key)
            currentValue = node_stub.hash_value_for_key(request_node)

            # check if node is the biggest
            if currentValue.hashValue > maxValue:
                maxValue = currentValue.hashValue
                champion_ip = node[0]
                champion_name = node[1]

        # creates a connection to the node
        channel = grpc.insecure_channel(champion_ip)
        node_stub = RN_pb2_grpc.RendezvousNodeStub(channel)

        # sends a the request to the node
        request = RN_pb2.NodeGetRequest(type, request.key, request.value)
        node_stub.get_request(request)


def serve(name, ip_address, port):
    channel = grpc.insecure_channel("172.17.0.2:50050")
    server_information_stub = SI_pb2_grpc.ServerInformationStub(channel)

    request = SI_pb2.AddRequest(
        type=SI_pb2.ROUTER, name=name, ip_address=f"{ip_address}:{port}"
    )
    _ = server_information_stub.add_(request)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    RH_pb2_grpc.add_RendezvousHashingServicer_to_server(RendezvousHashing(), server)
    server.add_insecure_port(f"{ip_address}:{port}")
    server.start()
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create Rendezvous Router.')
    parser.add_argument('--name', '-n', type=str, help='The name of the Router', default="router1")
    parser.add_argument('--port', '-p', type=int, help='The port of the Router', default=50151)
    args = parser.parse_args()
    
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    weight = 1
    print(f"starting Router '{args.name}': {ip_address}:{args.port}.")
    serve(args.name, ip_address, args.port)
