import argparse
import random
import socket
from collections import defaultdict
from concurrent import futures

import grpc
import src.grpc_enums.type_pb2 as type_pb2
import src.NamingService.NamingService_pb2 as NS_pb2
import src.NamingService.NamingService_pb2_grpc as NS_pb2_grpc
import src.Node.RendezvousNode_pb2 as RN_pb2
import src.Node.RendezvousNode_pb2_grpc as RN_pb2_grpc
import src.Router.RendezvousHashing_pb2 as RH_pb2
import src.Router.RendezvousHashing_pb2_grpc as RH_pb2_grpc
from src.Router.router_abstract import AbstractRouterClass

# look how to import from AbstractRouterClass since it is our abstract class. Maybe like this: RendezvousHashing(AbstractRouterClass(RH_pb2_grpc.RendezvousHashingServicer))
# DONE: inheriting from two classes at the same time could be done by separating them with a comma (nice one!)


class RendezvousHashing(AbstractRouterClass, RH_pb2_grpc.RendezvousHashingServicer):
    def __init__(self) -> None:
        channel = grpc.insecure_channel("172.17.0.2:50050")
        self.naming_service_stub = NS_pb2_grpc.NamingServiceStub(channel)
        # TODO: Locking this attribute to ensure sync
        self._dict_nodes = {}
        self.set_nodes()
        self.replica = 1

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

    def add_node(self, request, context):
        """
        adds a new Node into the Router.
        Also handles node balancing
        """

        request = NS_pb2.AddRequest(
            type=NS_pb2.NODE, name=request.name, ip_address=request.ip_address)
        self.naming_service_stub.add_(request)

        # redistributes object to the new node
        self.redistribute_objects_to_new_node(request.ip_address)

        return RH_pb2.RendezvousEmpty()

    def redistribute_objects_to_new_node(self, ip_address):
        """
        Redistributes all Key,Values of a all Nodes, if the new node is the champion

        node: the node that will be added
        """

        # TODO: threading?

        # loops over the ips and calls each node, to restribute their values to the new node
        # TODO: we currently dont look at replicas
        for n_ip in self._dict_nodes.copy().values():
            if n_ip == ip_address:
                continue

            # TODO: catch if we cant connect to the node
            channel = grpc.insecure_channel(n_ip)
            node_stub = RN_pb2_grpc.RendezvousNodeStub(channel)
            request = RN_pb2.NodeSendItemToNewNodeRequest(
                ip_address=ip_address)
            # sends a request to a node with the ip of the new node
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

        ip_address: the ip_address of the node that should be deleted
        """
        objects_on_node = defaultdict(list)
        channel = grpc.insecure_channel(ip_address)
        node_stub_del = RN_pb2_grpc.RendezvousNodeStub(channel)
        request = RN_pb2.NodeEmpty()
        responses = node_stub_del.get_objects(request)

        # reconstruct the dictionary of objects saved on the node
        for response in responses:
            objects_on_node[response.key].extend(response.values)

        # TODO: This solution is not efficient, we should use the node for this, but I'm not sure whether it's a design or programming issue.
        # TODO: replicas are currently not looked at
        for key, vs in objects_on_node.items():
            # find the champion
            champion_ip = self.find_responsible_node(
                key, self._dict_nodes.copy().items())[0]

            # connect to the champion
            channel = grpc.insecure_channel(champion_ip)
            node_stub = RN_pb2_grpc.RendezvousNodeStub(channel)

            # send a add request to the champion
            request = RN_pb2.NodeGetRequest(
                type=type_pb2.ADD, key=key, values=vs)
            node_stub.get_request(request)

        # clears the created dict
        objects_on_node.clear()
        # removes all elements
        node_stub_del.remove_all(RN_pb2.NodeEmpty())

    # TODO: Do Error if replicas+1 > total Nodes
    def forward_to_responsible_node(self, request, context):
        """
        finds the responsible node, for a given key
        and sende the the request to the node.

        key: the key of which we want to know the node

        return the Node for the given key
        """

        tmp_dict_items = self._dict_nodes.copy().items()

        if

        replica_unsure = False

        # if it is a get request, just take a subset
        if request.type == 1:
            ip_from_champions = self.find_responsible_node(request.key, random.sample(
                tmp_dict_items, len(tmp_dict_items)-self.replica))
            replica_unsure = True
        else:
            ip_from_champions = self.find_responsible_node(
                request.key, tmp_dict_items, self.replica)

        if len(ip_from_champions) > len(self._dict_nodes):
            print("ERROR: Number of requested replicas exceeds the number of available nodes")
            return None
        else:
            for id, ip in enumerate(ip_from_champions):
                # creates a connection
                channel = grpc.insecure_channel(ip)
                node_stub = RN_pb2_grpc.RendezvousNodeStub(channel)

                if not replica_unsure:
                    request = RN_pb2.NodeGetRequest(
                        type=request.type, key=request.key, values=request.values, replica_number=id)

                else:
                    request = RN_pb2.NodeGetRequest(
                        type=request.type, key=request.key, values=request.values, replica_number=-1)

                # sends the request to the node
                response = node_stub.get_request(request)

        if request.type != 1:
            return RH_pb2.RendezvousFindNodeResponse()

        else:
            fnd = RH_pb2.RendezvousFindNodeResponse(values=response.values)
            return fnd

    def find_responsible_node(self, key, dict_nodes_items, n_highest=0):
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
        return [tmp[0] for tmp in sorted(dict.items(), key=lambda x: x[1], reverse=True)[:n_highest+1]]


def serve(ip_address, port):
    # starts the grpc server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    RH_pb2_grpc.add_RendezvousHashingServicer_to_server(
        RendezvousHashing(), server)
    server.add_insecure_port(f"{ip_address}:{port}")
    server.start()
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    # arguments
    parser = argparse.ArgumentParser(description='Create Rendezvous Router.')
    parser.add_argument('--port', '-p', type=int,
                        help='The port of the Router', default=50151)
    args = parser.parse_args()

    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    print(f"starting Router: {ip_address}:{args.port}.")
    serve(ip_address, args.port)
