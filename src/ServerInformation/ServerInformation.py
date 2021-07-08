import time
from concurrent import futures
import random
import grpc
import argparse

import src.ServerInformation.ServerInformation_pb2 as ServerInformation_pb2
import src.ServerInformation.ServerInformation_pb2_grpc as ServerInformation_pb2_grpc

class ServerInformation(ServerInformation_pb2_grpc.ServerInformationServicer):
    lb_information = {}
    router_information = {}
    node_information = {}

    def add_(self, request, context):
        dict = self.get_dict(request.type)

        if dict is not False and request.name not in dict:
            dict[request.name] = request.ip_address
            return ServerInformation_pb2.AddReply(message="Add was successfull")
        return ServerInformation_pb2.AddReply(message="Add was not successfull")
    
    def get_(self, request, context):
        dict = self.get_dict(request.type)

        if dict is not False and request.name in dict:
            return ServerInformation_pb2.GetReply(ip_address=dict[request.name])
        return ServerInformation_pb2.GetReply(message="No IP-Address for this Name found")

    def get_random_(self, request, context):
        dict = self.get_dict(request.type)

        if dict is not False:
            item = random.choice(list(dict.items()))
            return ServerInformation_pb2.GetRandomReply(name=item[0],ip_address=item[1])
        return ServerInformation_pb2.GetRandomReply(message="No IP-Addresses are saved")

    def get_all_(self, request, context):
        dict = self.get_dict(request.type)

        if dict is not False:
            for name,ip in dict.items():
                yield ServerInformation_pb2.GetAllReply(name=name,ip_address=ip)
        else:
            return ServerInformation_pb2.GetAllReply(message="Operation was no successfull")


    def delete_(self, request, context):
        dict = self.get_dict(request.type)

        if dict is not False and request.name in dict:
            del dict[request.name]
            return ServerInformation_pb2.DeleteReply(message="Delete was successfull")
        return ServerInformation_pb2.DeleteReply(message="Delete was not successfull")

    def delete_all_(self, request, context):
        dict = self.get_dict(request.type)

        if dict is not False:
            dict.clear()
            return ServerInformation_pb2.DeleteAllReply(message="Delete was successfull")
        return ServerInformation_pb2.DeleteAllReply(message="Delete was not successfull")


    def get_dict(self, RequestType):
        if RequestType == 0:
            return self.lb_information
        elif RequestType == 1:
            return self.router_information
        elif RequestType == 2:
            return self.node_information
        return False


def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ServerInformation_pb2_grpc.add_ServerInformationServicer_to_server(ServerInformation(), server)
    server.add_insecure_port(f'0.0.0.0:{port}')
    server.start()
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create ServerInformation.')
    parser.add_argument('--port', '-p', type=int, help='The port of the ServerInformation', default=50050)
    args = parser.parse_args()
    serve(args.port)