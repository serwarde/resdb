import grpc
import random
import src.ServerInformation.ServerInformation_pb2 as SI_pb2
import src.ServerInformation.ServerInformation_pb2_grpc as SI_pb2_grpc
import src.Rendezvous.RendezvousHashing_pb2 as RH_pb2
import src.Rendezvous.RendezvousHashing_pb2_grpc as RH_pb2_grpc
import src.Rendezvous.RendezvousNode_pb2 as RN_pb2
import src.Rendezvous.RendezvousNode_pb2_grpc as RN_pb2_grpc

# DONE: refactor name
class LoadBalancer():
    
    def __init__(self):
        # connect to Server inforamtion server
        channel = grpc.insecure_channel('localhost:50050')
        self.server_information_stub = SI_pb2_grpc.ServerInformationStub(channel)

        # DONE: use a dict inside for each router with the attributes name, ip_address, port
        self._router_dict = {}

        # update the list of routers
        self.get_all_routers()
    
    def request(self,type,key,value=None):    
        '''
        gets a request from the user and calculates the responsible node
        and the forwards the request to this node
        
        type = can be (get, add, remove or update)
        key = the key for the item that should be stored
        value = only necessary for add and update
        '''

        # gets the router stub
        router_stub = self.get_random_router()

        # creates a request and gets the ip_address of a the responsible node
        request = RH_pb2.RendezvousFindNodeRequest(type=type, key=key, value=value)
        response = router_stub.forward_to_responsible_node(request)

        print(response)
        
    
    def get_random_router(self):
        """
        Return a random_router by choosing a random one from the local list
        """
        # TODO: Improve the strategy of choosing a router

        random_router = random.choice(list(self._router_dict.items()))
        channel = grpc.insecure_channel(random_router[0])

        return RH_pb2_grpc.RendezvousHashingStub(channel)


    # DONE: save the routers locally
    def get_all_routers(self):
        """
        Updated the list of all available routers from the ServerInformation
        """

        request = SI_pb2.GetAllRequest(type=SI_pb2.ROUTER)
        responses = self.server_information_stub.get_all_(request)
        for i, response in enumerate(responses):
            self._router_dict[response.name] = response.ip_address