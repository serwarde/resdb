import grpc
import src.grpc_enums.type_pb2 as type_pb2
import src.NamingService.NamingService_pb2 as NS_pb2
import src.NamingService.NamingService_pb2_grpc as NS_pb2_grpc
import src.Node.RendezvousNode_pb2 as RN_pb2
import src.Node.RendezvousNode_pb2_grpc as RN_pb2_grpc
import src.Router.RendezvousHashing_pb2 as RH_pb2
import src.Router.RendezvousHashing_pb2_grpc as RH_pb2_grpc


if __name__ == '__main__':
    c = grpc.insecure_channel('localhost:50251')
    node_stub0 = RN_pb2_grpc.RendezvousNodeStub(c)
    c = grpc.insecure_channel('localhost:50252')
    node_stub1 = RN_pb2_grpc.RendezvousNodeStub(c)
    c = grpc.insecure_channel('localhost:50253')
    node_stub2 = RN_pb2_grpc.RendezvousNodeStub(c)
    
    c = grpc.insecure_channel('localhost:50151')
    router_stub = RH_pb2_grpc.RendezvousHashingStub(c)
    
    c = grpc.insecure_channel('localhost:50050')
    naming_service_stub = NS_pb2_grpc.NamingServiceStub(c)
    
    request_ns = NS_pb2.AddRequest(
        type=NS_pb2.ROUTER, name="Router1", ip_address=f"172.17.0.3:50151")
    naming_service_stub.add_(request_ns)

    input("Press Enter to continue...")
    
    request = RH_pb2.RendezvousFindNodeRequest(
            type=type_pb2.ADD, key="SERWAR", values=["1"])
    router_stub.forward_to_responsible_node(request)

    request = RH_pb2.RendezvousFindNodeRequest(
            type=type_pb2.ADD, key="SERWAR", values=["2"])
    router_stub.forward_to_responsible_node(request)

    request = RH_pb2.RendezvousFindNodeRequest(
            type=type_pb2.ADD, key="SERWAR", values=["3"])
    router_stub.forward_to_responsible_node(request)

    request = RH_pb2.RendezvousFindNodeRequest(
            type=type_pb2.ADD, key="bob2", values=["2"])
    router_stub.forward_to_responsible_node(request)

    request = RH_pb2.RendezvousFindNodeRequest(
            type=type_pb2.ADD, key="bob3", values=["3"])
    router_stub.forward_to_responsible_node(request)

    request = RH_pb2.RendezvousFindNodeRequest(
            type=type_pb2.ADD, key="bob4", values=["4"])
    router_stub.forward_to_responsible_node(request)