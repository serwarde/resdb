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
from concurrent import futures

# TODO: look how to import from AbstractRouterClass since it is our abstract class. Maybe like this: RendezvousHashing(AbstractRouterClass(RH_pb2_grpc.RendezvousHashingServicer))
class RendezvousHashing(RH_pb2_grpc.RendezvousHashingServicer):
    ## TODO: Locking this attribute to ensure sync
    _list_of_nodes = []

    def __init__(self) -> None:
        channel = grpc.insecure_channel('172.17.0.2:50050')
        self.server_information_stub = SI_pb2_grpc.ServerInformationStub(channel)

    # TODO: add_node, remove_node are currently not working. they need to be callable by grpc. And also should update the ServerInformation
    # TODO: redistribute_objects_from_deleted_node, redistribute_objects_to_new_node should use grpc to call the nodes
    def add_node(self, node):
        """
        adds a new Node into the Router.
        Also handles node balancing

        node: the node that should be added
        """
        self._list_of_nodes.append(node)
        self.redistribute_objects_to_new_node(node)

    def remove_node(self, node):
        """
        removes a Node from the Router.
        Also handles node balancing

        node: the node that should be deleted
        """
        self._list_of_nodes.remove(node)
        self.redistribute_objects_from_deleted_node(node)        

    def find_responsible_node(self, request, context):
        """
        finds the responsible node, for a given key

        key: the key of which we want to know the node

        return the Node for the given key
        """
        champion_ip = None
        champion_name = None
        maxValue = -1

        # TODO: save nodes locally
        responses = self.server_information_stub.get_all_(SI_pb2.GetAllRequest(type=SI_pb2.NODE))

        # TODO: threading
        for node in responses:
            # connect to the node
            channel = grpc.insecure_channel(node.ip_address)
            node_stub = RN_pb2_grpc.RendezvousNodeStub(channel)

            # calc the hash score from the node
            request_node = RN_pb2.NodeHashValueForRequest(request.key)
            currentValue = node_stub.hash_value_for_key(request_node)

            # check if node is the biggest
            if currentValue.hashValue > maxValue:
                maxValue = currentValue.hashValue
                champion_ip = node.ip_address
                champion_name = node.name
        
        # return chamions ip 
        return RH_pb2_grpc.RendezvousFindNodeReply(name=champion_name,ip_address=champion_ip)

    def redistribute_objects_from_deleted_node(self, node):
        """
        Restributes all Key,Values of a deleted Node

        node: the node that should be deleted
        """
        for k,v in node.get_objects().items():
            self.find_responsible_node(k,v).add_object(k,v)
    
    def redistribute_objects_to_new_node(self, node):
        """
        Restributes all Key,Values of a all Nodes, if the new node is the champion

        node: the node that will be added
        """
        temp_list_of_nodes = self._list_of_node
        temp_list_of_nodes.remove(node)
        #TODO: threading?
        for n in temp_list_of_nodes:
            n.send_item_to_new_node(node)

def serve(name,ip_address,port):
    channel = grpc.insecure_channel('172.17.0.2:50050')
    server_information_stub = SI_pb2_grpc.ServerInformationStub(channel)

    request = SI_pb2.AddRequest(type=SI_pb2.ROUTER,name=name,ip_address=f'{ip_address}:{port}')
    _ = server_information_stub.add_(request)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    RH_pb2_grpc.add_RendezvousHashingServicer_to_server(RendezvousHashing(), server)
    server.add_insecure_port(f'{ip_address}:{port}')
    server.start()
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    name = "Router1"
    port = 50150
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    weight = 1
    print(f"starting Router '{name}': {ip_address}:{port}.")
    serve(name, ip_address, port)
