import time
from concurrent import futures

import grpc

import banking_pb2 
import banking_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Rerver(banking_pb2_grpc.BankingServicer):
    bank_balance = {}
    def CreateAccount(self, request, context):
        if request.name in self.bank_balance.keys():
            return banking_pb2.CreateReply(message="User has already an account")
        self.bank_balance[request.name] = request.money
        return banking_pb2.CreateReply(message="Accounted created successfully")
    
    def Add(self, request, context):
        new_balance = self.bank_balance[request.name] + request.money
        self.bank_balance[request.name] = new_balance
        return banking_pb2.AddReply(message=f"New Balance is now {new_balance}")

    def AddWOReturn(self, request, context):
        self.bank_balance[request.name] = self.bank_balance[request.name] + request.money
        return banking_pb2.AddWOReply()
    
    def Sub(self, request, context):
        new_balance = self.bank_balance[request.name] - request.money
        self.bank_balance[request.name] = new_balance
        return banking_pb2.SubReply(message=f"New Balance is now {new_balance}")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    banking_pb2_grpc.add_BankingServicer_to_server(Rerver(), server)
    server.add_insecure_port('0.0.0.0:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()