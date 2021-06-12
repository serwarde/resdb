import time
from concurrent import futures

import grpc

import src.Communication.grpc.idl_pb2 as idl_pb2
import src.Communication.grpc.idl_pb2_grpc as idl_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Rerver(idl_pb2_grpc.TimeServicer):
    def GetTime(self, request, context):
        return idl_pb2.TimeReply(message=time.ctime())
    def Add(self, n1, n2):
        return n1+n2


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    idl_pb2_grpc.add_TimeServicer_to_server(Rerver(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()