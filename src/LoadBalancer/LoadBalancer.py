import random

import grpc
import src.NamingService.NamingService_pb2 as NS_pb2
import src.NamingService.NamingService_pb2_grpc as NS_pb2_grpc
import src.Router.RendezvousHashing_pb2 as RH_pb2
import src.Router.RendezvousHashing_pb2_grpc as RH_pb2_grpc


# TODO: if LB is not grpc we need to use localhost instead of the ip
class LoadBalancer():
    
    def __init__(self):
        # connect to NamingService server
        channel = grpc.insecure_channel('localhost:50050')
        self.naming_service_stub = NS_pb2_grpc.NamingServiceStub(channel)

        # DONE: use a dict inside for each router with the attributes name, ip_address, port
        self._router_dict = {}

        # update the list of routers
        self.get_all_routers()
    
    # TODO: allow lists as value inputs, 
    # Todo: values should automatically transform to str
    def request(self,type, key: str, values=[]):    
        '''
        gets a request from the user and calculates the responsible node
        and the forwards the request to this node
        
        type = can be (get, add or remove)
        key = the key for the item that should be stored
        values = only necessary for add
        '''

        # gets the router stub
        router_stub = self.get_random_router()

        # TODO: check if all elements int he list have type bytes or unicode

        # creates a request and gets the ip_address of a the responsible node
        request = RH_pb2.RendezvousFindNodeRequest(type=type, key=key, values=values)
        response = router_stub.forward_to_responsible_node(request)

        if type == 1:
            return response
    
    def get_random_router(self):
        """
        Return a random_router by choosing a random one from the local list
        """
        # TODO: Improve the strategy of choosing a router

        random_router = random.choice(list(self._router_dict.values()))
        channel = grpc.insecure_channel(random_router)
        print(random_router)
        return RH_pb2_grpc.RendezvousHashingStub(channel)


    def get_all_routers(self):
        """
        Updated the list of all available routers from the NamingService
        """

        request = NS_pb2.GetAllRequest(type=NS_pb2.ROUTER)
        responses = self.naming_service_stub.get_all_(request)
        for response in responses:
            self._router_dict[response.name] = response.ip_address

    def add_node(self, name: str, ip_address: str, port: str):
        """
        Adds a node with the given name, ip:port.

        It sends the request to a random router where the node is added
        """
        # gets a router stub
        router_stub = self.get_random_router()

        # creates a request and gets the ip_address of a the responsible node
        request = RH_pb2.RendezvousInformation(name=name, ip_address=f"{ip_address}:{port}")
        router_stub.add_node(request)

    def remove_node(self, name: str, ip_address: str, port: str):
        """
        Removes a node with the given name, ip:port.

        It sends the request to a random router where the node is removed
        """

        # gets a router stub
        router_stub = self.get_random_router()

        # creates a request and gets the ip_address of a the responsible node
        request = RH_pb2.RendezvousInformation(name=name, ip_address=f"{ip_address}:{port}")
        router_stub.remove_node(request)

    # Local ip is needed as long the LB is not inside a docker container
    def add_router(self, name: str, ip_address: str, port: str, local_ip="localhost"):
        """
        Adds a Router with the given name, ip:port.

        It adds the router to the NamingService, and also in the local dict
        """

        request_ns = NS_pb2.AddRequest(type=NS_pb2.ROUTER, name=name, ip_address=f"{ip_address}:{port}")
        self.naming_service_stub.add_(request_ns)

        self._router_dict[name] = f"{local_ip}:{port}"

    def remove_router(self, name: str):
        """
        Removes a Router with the given name, ip:port.

        It removes the router from the NamingService, and also from the local dict
        """

        request_ns = NS_pb2.DeleteRequest(type=NS_pb2.ROUTER, name=name)
        self.naming_service_stub.delete_(request_ns)

        del self._router_dict[name]
