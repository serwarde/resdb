import grpc
import time

import ConsistentHashing_pb2 as pb2
import ConsistentHashing_pb2_grpc as pb2_grpc


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_ConsistentHashingServicer_to_server(node2, server)
    server.add_insecure_port('localhost:90002')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    server = node2
    serve()
