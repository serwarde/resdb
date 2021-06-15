import grpc

import banking_pb2 
import banking_pb2_grpc


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = banking_pb2_grpc.BankingStub(channel)


    request = banking_pb2.CreateRequest(name="Shan",money=400)
    response = stub.CreateAccount(request)
    print(response)

    request = banking_pb2.AddRequest(name="Shan",money=400)
    response = stub.Add(request)
    print(response)

    request = banking_pb2.SubRequest(name="Shan",money=400)
    response = stub.Sub(request)
    print(response)

    request = banking_pb2.CreateRequest(name="Shan",money=400)
    response = stub.CreateAccount(request)
    print(response)


if __name__ == '__main__':
    run()