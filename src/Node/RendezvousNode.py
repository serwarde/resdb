import argparse
import hashlib
import socket
from collections import defaultdict
from concurrent import futures
from typing import Union

import grpc
import src.grpc_enums.type_pb2 as type_pb2
import src.Node.RendezvousNode_pb2 as RN_pb2
import src.Node.RendezvousNode_pb2_grpc as RN_pb2_grpc
from src.Node.node_abstract import AbstractNodeClass


class RendezvousNode(AbstractNodeClass, RN_pb2_grpc.RendezvousNodeServicer):

    def __init__(self, ip_address, port, weight):
        self._host_ip = ip_address
        self._http_port = port
        self._node_weight = weight
        self._hashing = hashlib.md5
        self._objects_dict = defaultdict(list)
        self._replica_dict = defaultdict(lambda: defaultdict(list))

    def hash_value_for_key(self, request, context) -> float:
        """
        GRPC

        returns the hash for a given key. Uses sha256 for creating the hash value. In the
        hash function the seed is appended to key. The hash is then converted to int and then 
        multplied by the node weight
        """
        return RN_pb2.NodeHashValueForReply(hashValue=self.hash_value(request.key))

    # TODO: store hash values, to make it faster
    def hash_value(self, key) -> float:
        """
        returns the hash for a given key. Uses sha256 for creating the hash value. In the
        hash function the seed is appended to key. The hash is then converted to int and then 
        multplied by the node weight
        """
        hash = self._hashing((key+self._host_ip).encode('utf-8')).hexdigest()
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

        # copy dict, else we get an error, that the dict changed in size if we delete anything
        for key, vs in self._objects_dict.copy().items():
            # calculates the hash value for the new node

            request_node = RN_pb2.NodeHashValueForRequest(key=key)
            newNodeValue = node_stub.hash_value_for_key(request_node)

            # if the hashvalue from the new node is higher, send the key to the node
            if newNodeValue.hashValue >= self.hash_value(key):
                # we may have multiple values
                # TODO: maybe store hash values of the keys?

                request = RN_pb2.NodeGetRequest(
                    type=type_pb2.ADD, key=key, values=vs)
                node_stub.get_request(request)

                self.remove_object(key)

        return RN_pb2.NodeEmpty()

    def add_object(self, key, values, replica_number):
        """
        not GRPC

        adds a new object to the dict
        key = the key from the object
        value = value of the key

        TODO: extend to working with dicts as values
        """
        if not replica_number:
            self._objects_dict[key].extend(values)
        else:
            self._replica_dict[replica_number][key].extend(values)

    def remove_object(self, key, values=None, replica_number=0):
        """
        not GRPC

        removes a object from the dict, 
        if a value is given it just removes the value/s for the key

        key = the key from the object
        value = optional parameter, if a specific value/s should be deleted

        """
        if replica_number == 0:
            if key in self._objects_dict:
                if values:
                    for value in values:
                        try:
                            self._objects_dict[key].remove(value)
                        except ValueError:
                            pass  # do nothing if the value is not in the list
                else:
                    del self._objects_dict[key]

        else:
            if replica_number in self._replica_dict and key in self._replica_dict[replica_number]:
                if values:
                    for value in values:
                        try:
                            self._replica_dict[replica_number][key].remove(
                                value)
                        except ValueError:
                            pass  # do nothing if the value is not in the list
                else:
                    del self._replica_dict[replica_number][key]

    # DONE: delete update object since it is not needed

    def get_object(self, key, replica_number) -> Union[int, str, list, bool, tuple, dict]:
        """
        not GRPC

        returns the values for a given key
        key = the key from the object
        """
        if replica_number == 0:
            return self._objects_dict[key]
        elif replica_number > 0:
            return self._replica_dict[replica_number][key]
        elif replica_number == -1:
            values = self._objects_dict[key]
            if values:
                return

            for replica in self._replica_dict.copy().values():
                if key in self._replica_dict[replica].keys():
                    return self._replica_dict[replica][key]

        return []

    def get_objects(self, request, context) -> dict:
        """
        GRPC
        returns all main keys in node
        """
        yield RN_pb2.NodeGetObjectsReply(key="NONE", values=list(self._objects_dict.copy()))

    def get_replicas(self, request, context) -> dict:
        """
        GRPC
        returns all replica keys in node
        """
        for kv_pairs in self._replica_dict.copy().values():
            yield RN_pb2.NodeGetObjectsReply(key="NONE", values=list(kv_pairs.copy()))

    def remove_all(self, request, context):
        self._objects_dict.clear()
        self._replica_dict.clear()
        return RN_pb2.NodeEmpty()

    def get_request(self, request, context):
        """
        GRPC

        Node gets a request, checks the type of the request and calls the responsible function

        type = can be (get, add, remove or update)
        key = the key for the item that should be stored
        value = only necessary for add and update
        """

        print("object: ", self._objects_dict)
        print("replica: ", self._replica_dict)

        # add request
        if request.type == 0:
            self.add_object(request.key, request.values,
                            request.replica_number)
            return RN_pb2.NodeGetReply()

        # get request
        elif request.type == 1:
            # get request can be in either dictonary
            ngr = RN_pb2.NodeGetReply(values=self.get_object(
                request.key, request.replica_number))
            return ngr

        # delete request
        elif request.type == 2:
            self.remove_object(request.key, request.values,
                               request.replica_number)
            return RN_pb2.NodeGetReply()


def serve(ip_address, port, weight):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    RN_pb2_grpc.add_RendezvousNodeServicer_to_server(
        RendezvousNode(ip_address, port, weight), server)
    server.add_insecure_port(f'{ip_address}:{port}')
    server.start()
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create Rendezvous Node.')
    parser.add_argument('--port', '-p', type=int,
                        help='The port of the Node', default=50251)
    parser.add_argument('--weight', '-w', type=float,
                        help='The weight of the Node', default=1.0)
    args = parser.parse_args()

    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    print(f"starting Node: {ip_address}:{args.port} with {args.weight}.")
    serve(ip_address, args.port, args.weight)
