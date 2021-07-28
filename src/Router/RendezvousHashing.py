from src.Node.RendezvousNode import RendezvousNode
from src.Router.router_abstract import AbstractRouterClass

import src.NamingService.NamingService_pb2 as NS_pb2
import src.NamingService.NamingService_pb2_grpc as NS_pb2_grpc

import src.Router.RendezvousHashing_pb2 as RH_pb2
import src.Router.RendezvousHashing_pb2_grpc as RH_pb2_grpc

import src.Node.RendezvousNode_pb2 as RN_pb2
import src.Node.RendezvousNode_pb2_grpc as RN_pb2_grpc

import src.grpc_enums.type_pb2 as type_pb2

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
        self.naming_service_stub = NS_pb2_grpc.NamingServiceStub(channel)
        ## TODO: Locking this attribute to ensure sync
        self._dict_nodes = {}
        self.set_nodes()
        self.replica = 2

    def set_nodes(self):
        """
        Updated the list of all available nodes from the NamingService
        """
        request = NS_pb2.GetAllRequest(type=NS_pb2.NODE)
        responses = self.naming_service_stub.get_all_(request)
        for response in responses:
            self._dict_nodes[response.name] = response.ip_address

    def _add_node(self, request, context):
        """
        should only be called by the NamingService

        it adds the node into the local dictonary
        """

        self._dict_nodes[request.name] = request.ip_address
        return RH_pb2.RendezvousEmpty()

    # TODO: if we use multiple routers, we need to ensure that all of them have the same _dict_nodes, currently its gets only updated in the init.
    # TODO: Serverinfomration send an update when a node gets added or deleted
    # TODO: add paramerter so we can use this function to update the information in all routers
    def add_node(self, request, context):
        """
        adds a new Node into the Router.
        Also handles node balancing

        node: the node that should be added
        """
        
        request = NS_pb2.AddRequest(type=NS_pb2.NODE,name=request.name,ip_address=request.ip_address)
        self.naming_service_stub.add_(request)

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

    def _remove_node(self, request, context):
        """
        should only be called by the NamingService

        it removes the node from the local dictonary
        """

        del self._dict_nodes[request.name]
        return RH_pb2.RendezvousEmpty()


    def remove_node(self, request, context):
        """
        removes a Node from the Router.
        Also handles node balancing

        node: the node that should be deleted
        """
        # TODO: check if node with ip is in the list

        request_sis = NS_pb2.DeleteRequest(type=NS_pb2.NODE, name=request.name)
        self.naming_service_stub.delete_(request_sis)
        
        self.redistribute_objects_from_deleted_node(request.ip_address)
        return RH_pb2.RendezvousEmpty()

    def redistribute_objects_from_deleted_node(self, ip_address):
        """
        Redistributes all Key,Values of a deleted Node

        node: the node that should be deleted
        """
        objects_on_node = defaultdict(list)
        channel = grpc.insecure_channel(ip_address)
        node_stub_del = RN_pb2_grpc.RendezvousNodeStub(channel)
        request = RN_pb2.NodeEmpty()
        responses = node_stub_del.get_objects(request)

        # reconstruct the dictionary of objects saved on the node
        for response in responses:
            objects_on_node[response.key].append(response.value)

        # TODO: This solution is not efficient, we should use the node for this
        # , but I'm not sure whether it's a design or programming issue. 
        # TODO: currently not replicas are used
        for key, vs in objects_on_node.items():
            champion_ip = self.find_responsible_node(key, self._dict_nodes.copy().items())[0]
            
            channel = grpc.insecure_channel(champion_ip)
            node_stub = RN_pb2_grpc.RendezvousNodeStub(channel)

            for v in vs:
                request = RN_pb2.NodeGetRequest(type=type_pb2.ADD,key=key,value=v)
                node_stub.get_request(request)

        objects_on_node.clear()
        node_stub_del.remove_all(RN_pb2.NodeEmpty())

    # TODO: currently gets are not returned
    # TODO: for gets we can use a smaller list
    def forward_to_responsible_node(self, request, context):
        """
        finds the responsible node, for a given key
        and sende the the request to the node.

        key: the key of which we want to know the node

        return the Node for the given key
        """

        ip_from_champions = self.find_responsible_node(request.key, self._dict_nodes.copy().items())
       
        champion = True

        for ip in ip_from_champions:
            # creates a connection  
            channel = grpc.insecure_channel(ip)
            node_stub = RN_pb2_grpc.RendezvousNodeStub(channel)

            if champion:
                request = RN_pb2.NodeGetRequest(type=request.type, key=request.key, value=request.value)
                champion = False
            else:
                request = RN_pb2.NodeGetRequest(type=request.type, key=request.key, value=request.value, replica=True)
            
            # sends the request to the node
            node_stub.get_request(request)

        return RH_pb2.RendezvousEmpty()

    def find_responsible_node(self, key, dict_nodes_items, replica=1):
        dict = {}

        # TODO: threading
        for _, n_ip in dict_nodes_items:
            # note: a node tuple consists of an ip_address and name
            # connect to the node
            channel = grpc.insecure_channel(n_ip)
            node_stub = RN_pb2_grpc.RendezvousNodeStub(channel)

            # calc the hash score from the node
            request_node = RN_pb2.NodeHashValueForRequest(key=key)
            currentValue = node_stub.hash_value_for_key(request_node)

            dict[n_ip] = currentValue.hashValue

        # sorts the dict based on the hashValue and then returns the ip of the highest hashvalues.
        # It is in order therefore is the first node the champion
        return [tmp[0] for tmp in sorted(dict.items(), key=lambda x: x[1], reverse=True)[:replica]]

def serve(ip_address, port):
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
    parser.add_argument('--port', '-p', type=int, help='The port of the Router', default=50151)
    args = parser.parse_args()
    
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    
    print(f"starting Router: {ip_address}:{args.port}.")
    serve(ip_address, args.port)
