import grpc
import src.ServerInformation.ServerInformation_pb2 as SI_pb2
import src.ServerInformation.ServerInformation_pb2_grpc as SI_pb2_grpc
import src.Rendezvous.RendezvousHashing_pb2 as RH_pb2
import src.Rendezvous.RendezvousHashing_pb2_grpc as RH_pb2_grpc
import src.Rendezvous.RendezvousNode_pb2 as RN_pb2
import src.Rendezvous.RendezvousNode_pb2_grpc as RN_pb2_grpc

# TODO: make to a grpc server?
class LoadBalancer():
    
    def __init__(self):
        # connect to Server inforamtion server
        channel = grpc.insecure_channel('localhost:50050')
        self.server_information_stub = SI_pb2_grpc.ServerInformationStub(channel)

        # TODO: use a dict inside for each router with the attributes name, ip_address, port
        self._router_dict = {}
    
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
        request = RH_pb2.RendezvousFindNodeRequest(key)
        response = router_stub.find_responsible_node(request)
        
        # TODO: why do this here, just send the request from the node or the hashring (router)
        
        # creates a connection to the node
        channel = grpc.insecure_channel(response.ip_address)
        node_stub = RN_pb2_grpc.RendezvousNodeStub(channel)
        
        # sends a the request to the node
        request = RN_pb2.NodeGetRequest(type, key, value)
        node_stub.get_request(request)
    
    # TODO: save the routers locally
    def get_random_router(self):
        """
        Return a random_router
        """
        # TODO: Improve the strategy of choosing a router
        request = SI_pb2.GetRandomRequest(type=SI_pb2.ROUTER)
        response = self.server_information_stub.get_random_(request)

        channel = grpc.insecure_channel(response.ip_address)

        return RH_pb2_grpc.RendezvousHashingStub(channel)
    
    def get_router_list(self):
        """
        Returns the router_list
        """
        return self._router_dict