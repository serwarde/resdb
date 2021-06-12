import grpc

import src.Communication.grpc.idl_pb2 as idl_pb2
import src.Communication.grpc.idl_pb2_grpc as idl_pb2_grpc


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = idl_pb2_grpc.TimeStub(channel)
    response = stub.GetTime(idl_pb2.TimeRequest())
    print('Client received: {}'.format(response.message))


if __name__ == '__main__':
    run()