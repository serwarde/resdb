from src.Node.node_abstract import AbstractNodeClass
from typing import DefaultDict, Union
from collections import defaultdict

import hashlib
import socket
import argparse

import src.Rendezvous.RendezvousNode_pb2 as RN_pb2
import src.Rendezvous.RendezvousNode_pb2_grpc as RN_pb2_grpc
import src.ServerInformation.ServerInformation_pb2 as SI_pb2
import src.ServerInformation.ServerInformation_pb2_grpc as SI_pb2_grpc

import src.Rendezvous.type_pb2 as type_pb2

import grpc
from concurrent import futures

# TODO: look how to import from AbstractNodeClass since it is our abstract class. Maybe like this: RendezvousNode(AbstractNodeClass(RN_pb2_grpc.RendezvousNodeServicer))
class RendezvousNode(RN_pb2_grpc.RendezvousNodeServicer):

    def __init__(self, name, ip_address, port, weight):
        self._host_name = name
        self._host_ip = ip_address
        self._http_port = port
        self._node_weight = weight
        self._hashing = hashlib.md5
        # TODO: Check if ip_address is a adequate seed for the node
        self._node_seed = str(ip_address)+str(name)
        # TODO: Check if a list is a good representation for values
        self._objects_dict = defaultdict(list)

    def hash_value_for_key(self, request, context) -> float:
        """
        GRPC

        returns the hash for a given key. Uses sha256 for creating the hash value. In the
        hash function the seed is appended to key. The hash is then converted to int and then 
        multplied by the node weight
        """
        return RN_pb2.NodeHashValueForReply(hashValue=self.hash_value(request.key))

    def hash_value(self, key) -> float:
        """
        returns the hash for a given key. Uses sha256 for creating the hash value. In the
        hash function the seed is appended to key. The hash is then converted to int and then 
        multplied by the node weight
        """
        hash = self._hashing((key+self._host_ip).encode('utf-8')).hexdigest()
        final_hash = float.fromhex(hash) * self._node_weight
        return float.fromhex(hash) * self._node_weight

    # Done: implement as a GRPC function. Since it needs to connect to the other node.
    def send_item_to_new_node(self, request, context):
        """
        GRPC

        this function is called when we add a new node. It loops over all keys in its own 
        dict and checks if the hashValue of the new Node is higher then the own. If yes it 
        sends the key, value pair to the new node, where it now is stored. After sending it 
        deletes the kv-pair in the own dictionary
        """

        channel = grpc.insecure_channel(request.ip_address)
        node_stub = RN_pb2_grpc.RendezvousNodeStub(channel)

        # we need to copy, else we get an error, that the dict changed in size if we delete anything
        for k,vs in self._objects_dict.copy().items():
            request_node = RN_pb2.NodeHashValueForRequest(key=k)
            newNodeValue = node_stub.hash_value_for_key(request_node)

            if newNodeValue.hashValue >= self.hash_value(k):

                # we may have multiple values
                # TODO: use stream instead of unique calls
                # TODO: maybe store hash values of the keys?
                for v in vs:
                    request = RN_pb2.NodeGetRequest(type=type_pb2.ADD,key=k,value=v)
                    responses = node_stub.get_request(request)

                    for _ in responses:
                        pass

                self.remove_object(k)

        return RN_pb2.NodeEmpty()
                

    def add_object(self, key, value):
        """
        not GRPC

        adds a new object to the dict
        key = the key from the object
        value = value of the key

        TODO: extend to working with dicts as values
        """
        self._objects_dict[key].append(value)

    def remove_object(self, key, value=None):
        """
        not GRPC

        removes a object from the dict, 
        if a value is given it just removes the value/s for the key
        
        key = the key from the object
        value = optional parameter, if a specific value/s should be deleted
        """
        if key in self._objects_dict:
            if value:
                try:
                    self._objects_dict[key].remove(value)
                except ValueError:
                    pass # do nothing if the value is not in the list
            else:
                del self._objects_dict[key]

    def update_object(self, key, value):
        """
        not GRPC

        updates a object in the dict, 
        if a dict, list or tuple is used we append the value/s to the key
        key = the key from the object
        value = value of the key

        TODO: Check if necessary if we keep using lists as values in the defaultdict
        """
        self._objects_dict[key].append(value)
    
    def get_object(self, key) -> Union[int,str,list,bool,tuple,dict]:
        """
        not GRPC

        returns the values for a given key
        key = the key from the object
        """
        return self._objects_dict[key]

    # TODO: implement as GRPC
    def get_objects(self) -> dict:
        """
        not GRPC

        returns all objects in node
        """
        return self._objects_dict
    
    def get_request(self, request, context):
        """
        GRPC

        Node gets a request, checks the type of the request and calls the responsible function
        
        type = can be (get, add, remove or update)
        key = the key for the item that should be stored
        value = only necessary for add and update
        """
        print(self._objects_dict)

        if request.type == 0:
            self.add_object(request.key,request.value)
            return RN_pb2.NodeGetReply()
        elif request.type == 1:
            self.update_object(request.key,request.value)
            return RN_pb2.NodeGetReply()
        elif request.type == 2:
            for value in self.get_object(request.key):
                yield RN_pb2.NodeGetReply(value=value)
        elif request.type == 3:
            self.remove_object(request.key,request.value)
            return RN_pb2.NodeGetReply()
        
        
        

def serve(name, ip_address, port, weight):
    channel = grpc.insecure_channel('172.17.0.2:50050')
    server_information_stub = SI_pb2_grpc.ServerInformationStub(channel)
    request = SI_pb2.AddRequest(type=SI_pb2.NODE,name=name,ip_address=f'{ip_address}:{port}')
    _ = server_information_stub.add_(request)


    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    RN_pb2_grpc.add_RendezvousNodeServicer_to_server(RendezvousNode(name, ip_address, port, weight), server)
    server.add_insecure_port(f'{ip_address}:{port}')
    server.start()
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create Rendezvous Node.')
    parser.add_argument('--name', '-n', type=str, help='The name of the Node', default="node1")
    parser.add_argument('--port', '-p', type=int, help='The port of the Node', default=50251)
    parser.add_argument('--weight', '-w', type=float, help='The weight of the Node', default=1.0)
    args = parser.parse_args()

    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    
    print(f"starting Node '{args.name}': {ip_address}:{args.port} with {args.weight}.")
    serve(args.name, ip_address, args.port, args.weight)
