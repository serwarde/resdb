import time
from concurrent import futures
import random
import grpc
import argparse

import src.NamingService.NamingService_pb2 as NamingService_pb2
import src.NamingService.NamingService_pb2_grpc as NamingService_pb2_grpc

import src.Rendezvous.RendezvousHashing_pb2 as RH_pb2
import src.Rendezvous.RendezvousHashing_pb2_grpc as RH_pb2_grpc

class NamingService(NamingService_pb2_grpc.NamingServiceServicer):
    lb_information = {}
    router_information = {}
    node_information = {}

    def add_(self, request, context):
        """
        adds a entry into the corresponding dict
        """

        dict = self.get_dict(request.type)

        if dict is not False and request.name not in dict:
            dict[request.name] = request.ip_address
            
            # if we add a new node send update to each router
            if request.type == 2:
                for router_ip in self.router_information.copy().values():
                    channel = grpc.insecure_channel(router_ip)
                    router_stup = RH_pb2_grpc.RendezvousHashingStub(channel)
                    request = RH_pb2.RendezvousInformation(name=request.name,ip_address=request.ip_address) 
                    router_stup._add_node(request)

            return NamingService_pb2.AddReply(message="Add was successfull")

        return NamingService_pb2.AddReply(message="Add was not successfull")
    
    def get_(self, request, context):
        """
        return a entry from the corresponding dict
        """

        dict = self.get_dict(request.type)

        if dict is not False and request.name in dict:
            return NamingService_pb2.GetReply(ip_address=dict[request.name])
        return NamingService_pb2.GetReply(message="No IP-Address for this Name found")

    def get_random_(self, request, context):
        """
        return a random entry from the corresponding dict
        """

        dict = self.get_dict(request.type)

        if dict is not False:
            item = random.choice(list(dict.items()))
            return NamingService_pb2.GetRandomReply(name=item[0],ip_address=item[1])
        return NamingService_pb2.GetRandomReply(message="No IP-Addresses are saved")

    def get_all_(self, request, context):
        """
        return all entries from the corresponding dict
        """

        dict = self.get_dict(request.type)

        if dict is not False:
            for name,ip in dict.items():
                yield NamingService_pb2.GetAllReply(name=name,ip_address=ip)
        else:
            return NamingService_pb2.GetAllReply(message="Operation was no successfull")


    def delete_(self, request, context):
        """
        deletes a entry from the corresponding dict
        """

        dict = self.get_dict(request.type)

        if dict is not False and request.name in dict:
            del dict[request.name]

            # if we delete a new node send update to each router
            if request.type == 2:
                for router_ip in self.router_information.copy().values():
                    channel = grpc.insecure_channel(router_ip)
                    router_stup = RH_pb2_grpc.RendezvousHashingStub(channel)
                    request = RH_pb2.RendezvousInformation(name=request.name) 
                    router_stup._remove_node(request)

            return NamingService_pb2.DeleteReply(message="Delete was successfull")
        return NamingService_pb2.DeleteReply(message="Delete was not successfull")

    def delete_all_(self, request, context):
        """
        deletes all entries from the corresponding dict
        """

        dict = self.get_dict(request.type)

        if dict is not False:
            dict.clear()
            return NamingService_pb2.DeleteAllReply(message="Delete was successfull")
        return NamingService_pb2.DeleteAllReply(message="Delete was not successfull")


    def get_dict(self, RequestType):
        """
        returns the correct dictonary bases on the RequestType
        """

        if RequestType == 0:
            return self.lb_information
        elif RequestType == 1:
            return self.router_information
        elif RequestType == 2:
            return self.node_information
        return False


def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    NamingService_pb2_grpc.add_NamingServiceServicer_to_server(NamingService(), server)
    server.add_insecure_port(f'0.0.0.0:{port}')
    server.start()
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create NamingService.')
    parser.add_argument('--port', '-p', type=int, help='The port of the NamingService', default=50050)
    args = parser.parse_args()
    serve(args.port)