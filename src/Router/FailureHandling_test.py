import grpc
import src.grpc_enums.type_pb2 as type_pb2
import src.NamingService.NamingService_pb2 as NS_pb2
import src.NamingService.NamingService_pb2_grpc as NS_pb2_grpc
import src.Node.RendezvousNode_pb2 as RN_pb2
import src.Node.RendezvousNode_pb2_grpc as RN_pb2_grpc
import src.Router.RendezvousHashing_pb2 as RH_pb2
import src.Router.RendezvousHashing_pb2_grpc as RH_pb2_grpc

if __name__ == '__main__':

    """
    Initialize nodes, router and namingService
    """

    channel = grpc.insecure_channel('localhost:50251')
    node_stub0 = RN_pb2_grpc.RendezvousNodeStub(channel)
    channel = grpc.insecure_channel('localhost:50252')
    node_stub1 = RN_pb2_grpc.RendezvousNodeStub(channel)
    channel = grpc.insecure_channel('localhost:50253')
    node_stub2 = RN_pb2_grpc.RendezvousNodeStub(channel)
    channel = grpc.insecure_channel('localhost:50254')
    node_stub3 = RN_pb2_grpc.RendezvousNodeStub(channel)
    channel = grpc.insecure_channel('localhost:50255')
    node_stub4 = RN_pb2_grpc.RendezvousNodeStub(channel)
    channel = grpc.insecure_channel('localhost:50256')
    node_stub5 = RN_pb2_grpc.RendezvousNodeStub(channel)

    channel = grpc.insecure_channel('localhost:50151')
    router_stub = RH_pb2_grpc.RendezvousHashingStub(channel)

    channel = grpc.insecure_channel('localhost:50050')
    naming_service_stub = NS_pb2_grpc.NamingServiceStub(channel)

    request_ns = NS_pb2.AddRequest(
        type=NS_pb2.ROUTER, name="Router1", ip_address=f"172.17.0.3:50151")
    naming_service_stub.add_(request_ns)

    """
    Add the nodes to the router
    """

    request = RH_pb2.RendezvousInformation(
        name="node0", ip_address="172.17.0.4:50251")
    router_stub.add_node(request)

    request = RH_pb2.RendezvousInformation(
        name="node1", ip_address="172.17.0.5:50252")
    router_stub.add_node(request)

    request = RH_pb2.RendezvousInformation(
        name="node2", ip_address="172.17.0.6:50253")
    router_stub.add_node(request)

    request = RH_pb2.RendezvousInformation(
        name="node3", ip_address="172.17.0.7:50254")
    router_stub.add_node(request)

    request = RH_pb2.RendezvousInformation(
        name="node4", ip_address="172.17.0.8:50255")
    router_stub.add_node(request)

    request = RH_pb2.RendezvousInformation(
        name="node5", ip_address="172.17.0.9:50256")
    router_stub.add_node(request)


    """
    Add some key-value-pairs to the network
    """
    request = RH_pb2.RendezvousFindNodeRequest(
        type=type_pb2.ADD, key="Sam", values=["14"])
    router_stub.forward_to_responsible_node(request)

    request = RH_pb2.RendezvousFindNodeRequest(
        type=type_pb2.ADD, key="bob1", values=["14"])
    router_stub.forward_to_responsible_node(request)

    request = RH_pb2.RendezvousFindNodeRequest(
        type=type_pb2.ADD, key="Nico", values=["14", "78"])
    router_stub.forward_to_responsible_node(request)

    request = RH_pb2.RendezvousFindNodeRequest(
        type=type_pb2.ADD, key="Tina", values=["64", "10", "11"])
    router_stub.forward_to_responsible_node(request)

    request = RH_pb2.RendezvousFindNodeRequest(
            type=type_pb2.ADD, key="bob2", values=["11"])
    router_stub.forward_to_responsible_node(request)

    request = RH_pb2.RendezvousFindNodeRequest(
            type=type_pb2.ADD, key="Michelle", values=["22", "99"])
    router_stub.forward_to_responsible_node(request)

    request = RH_pb2.RendezvousFindNodeRequest(
            type=type_pb2.ADD, key="Tammy", values=["33", "00"])
    router_stub.forward_to_responsible_node(request)

    request = RH_pb2.RendezvousFindNodeRequest(
            type=type_pb2.ADD, key="Mark", values=["44", "19"])
    router_stub.forward_to_responsible_node(request)

    request = RH_pb2.RendezvousFindNodeRequest(
            type=type_pb2.ADD, key="Brad", values=["55"])
    router_stub.forward_to_responsible_node(request)

    request = RH_pb2.RendezvousFindNodeRequest(
            type=type_pb2.ADD, key="Cassie", values=["66"])
    router_stub.forward_to_responsible_node(request)

    input("Stop one of the Node docker containers then press Enter to continue...")

    try:
        request = RH_pb2.RendezvousFindNodeRequest(
                type=type_pb2.ADD, key="bob2", values=["111"])
        router_stub.forward_to_responsible_node(request)

        request = RH_pb2.RendezvousFindNodeRequest(
                type=type_pb2.ADD, key="Michelle", values=["222"])
        router_stub.forward_to_responsible_node(request)

        request = RH_pb2.RendezvousFindNodeRequest(
                type=type_pb2.ADD, key="Tammy", values=["333"])
        router_stub.forward_to_responsible_node(request)

        request = RH_pb2.RendezvousFindNodeRequest(
                type=type_pb2.ADD, key="Mark", values=["444"])
        router_stub.forward_to_responsible_node(request)

        request = RH_pb2.RendezvousFindNodeRequest(
                type=type_pb2.ADD, key="Brad", values=["555"])
        router_stub.forward_to_responsible_node(request)

        request = RH_pb2.RendezvousFindNodeRequest(
                type=type_pb2.ADD, key="Cassie", values=["666"])
        router_stub.forward_to_responsible_node(request)
    except grpc.RpcError as e:
        print("Server unavialable, request was not handled.")