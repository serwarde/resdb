import unittest

import grpc
import src.grpc_enums.type_pb2 as type_pb2
import src.NamingService.NamingService_pb2 as NS_pb2
import src.NamingService.NamingService_pb2_grpc as NS_pb2_grpc
import src.Node.RendezvousNode_pb2 as RN_pb2
import src.Node.RendezvousNode_pb2_grpc as RN_pb2_grpc
import src.Router.RendezvousHashing_pb2 as RH_pb2
import src.Router.RendezvousHashing_pb2_grpc as RH_pb2_grpc


class TestRendezvousNodeMethods(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestRendezvousNodeMethods, self).__init__(*args, **kwargs)
        channel = grpc.insecure_channel('localhost:50251')
        self.node_stub0 = RN_pb2_grpc.RendezvousNodeStub(channel)
        channel = grpc.insecure_channel('localhost:50252')
        self.node_stub1 = RN_pb2_grpc.RendezvousNodeStub(channel)
        channel = grpc.insecure_channel('localhost:50253')
        self.node_stub2 = RN_pb2_grpc.RendezvousNodeStub(channel)
        channel = grpc.insecure_channel('localhost:50151')
        self.router_stub = RH_pb2_grpc.RendezvousHashingStub(channel)
        channel = grpc.insecure_channel('localhost:50050')
        self.naming_service_stub = NS_pb2_grpc.NamingServiceStub(channel)
        request_ns = NS_pb2.AddRequest(
            type=NS_pb2.ROUTER, name="Router1", ip_address=f"172.17.0.3:50151")
        self.naming_service_stub.add_(request_ns)

    def test1_add_node(self):
        request = RH_pb2.RendezvousInformation(
            name="node0", ip_address="172.17.0.4:50251")
        self.router_stub.add_node(request)

        # adds some values to the first server
        self.add_helper()
        # check if all values are added to node0
        self.tst_value_for_key("Sam", ["14"])
        self.tst_value_for_key("bob1", ["34"])
        self.tst_value_for_key("Nico", ["54", "612"])
        self.tst_value_for_key("Serwar", ["54"])

        # adds two more nodes
        request = RH_pb2.RendezvousInformation(
            name="node1", ip_address="172.17.0.5:50252")
        self.router_stub.add_node(request)
        request = RH_pb2.RendezvousInformation(
            name="node2", ip_address="172.17.0.6:50253")
        self.router_stub.add_node(request)

        # check if the values got redistributed
        self.tst_value_for_key("Sam", ["14"])
        self.tst_value_for_key("bob1", ["34"], 1)
        self.tst_value_for_key("Nico", ["54", "612"], 2)
        self.tst_value_for_key("Serwar", ["54"], 2)

        # deletes the values
        self.del_helper()

    def test2_find_responsible_node(self):
        # add KV for Sam. Sam is saved at Node0
        request = RH_pb2.RendezvousFindNodeRequest(
            type=type_pb2.ADD, key="Sam", values=["14"])
        self.router_stub.forward_to_responsible_node(request)
        self.tst_value_for_key("Sam", ["14"])
        self.tst_value_for_key("Sam", ["14"],2,1)

        # delete KV for Sam. Sam is saved at Node0
        request = RH_pb2.RendezvousFindNodeRequest(
            type=type_pb2.DELETE, key="Sam", values=["14"])
        self.router_stub.forward_to_responsible_node(request)
        self.tst_value_for_key("Sam", [])
        self.tst_value_for_key("Sam", [],2,1)

        # add KV for bob1. bob1 is saved at Node1
        request = RH_pb2.RendezvousFindNodeRequest(
            type=type_pb2.ADD, key="bob1", values=["14"])
        self.router_stub.forward_to_responsible_node(request)
        self.tst_value_for_key("bob1", ["14"], 1)
        self.tst_value_for_key("bob1", ["14"], 2,1)

        # delete KV for bob1. bob1 is saved at Node1
        request = RH_pb2.RendezvousFindNodeRequest(
            type=type_pb2.DELETE, key="bob1", values=["14"])
        self.router_stub.forward_to_responsible_node(request)
        self.tst_value_for_key("bob1", [], 1)
        self.tst_value_for_key("bob1", [], 2,1)

        # add KV for Nico. Nico is saved at Node2
        request = RH_pb2.RendezvousFindNodeRequest(
            type=type_pb2.ADD, key="Nico", values=["14", "78", "211", "1"])
        self.router_stub.forward_to_responsible_node(request)
        self.tst_value_for_key("Nico", ["14", "78", "211", "1"], 2)
        self.tst_value_for_key("Nico", ["14", "78", "211", "1"], 1, 1)

        # delete KV for Nico. Nico is saved at Node2
        request = RH_pb2.RendezvousFindNodeRequest(
            type=type_pb2.DELETE, key="Nico", values=["14", "78", "211", "1", "45"])
        self.router_stub.forward_to_responsible_node(request)
        self.tst_value_for_key("Nico", [], 2)
        self.tst_value_for_key("Nico", [], 1, 1)

    def test3_remove_node(self):
        # add KV for Sam. Sam is saved at Node0
        request = RH_pb2.RendezvousFindNodeRequest(
            type=type_pb2.ADD, key="Sam", values=["14"])
        self.router_stub.forward_to_responsible_node(request)
        self.tst_value_for_key("Sam", ["14"])

        # add KV for bob1. bob1 is saved at Node1
        request = RH_pb2.RendezvousFindNodeRequest(
            type=type_pb2.ADD, key="bob1", values=["14"])
        self.router_stub.forward_to_responsible_node(request)
        self.tst_value_for_key("bob1", ["14"], 1)

        # add KV for Nico. Nico is saved at Node2
        request = RH_pb2.RendezvousFindNodeRequest(
            type=type_pb2.ADD, key="Nico", values=["14"])
        self.router_stub.forward_to_responsible_node(request)
        self.tst_value_for_key("Nico", ["14"], 2)

        # remove node
        request = RH_pb2.RendezvousInformation(
            name="node2", ip_address="172.17.0.6:50253")
        self.router_stub.remove_node(request)
        self.tst_value_for_key("Nico", ["14"], 1)
        self.tst_value_for_key("bob1", ["14"], 1)
        self.tst_value_for_key("Nico", [], 2)

        request = RH_pb2.RendezvousInformation(
            name="node1", ip_address="172.17.0.5:50252")
        self.router_stub.remove_node(request)
        self.tst_value_for_key("Sam", ["14"])
        self.tst_value_for_key("Nico", ["14"])
        self.tst_value_for_key("bob1", ["14"])
        self.tst_value_for_key("bob1", [], 1)
        self.tst_value_for_key("Nico", [], 1)

    def tst_value_for_key(self, key, values, stub=0, storage=0):

        request = RN_pb2.NodeGetRequest(type=type_pb2.GET, key=key, replica_number=storage)
        if stub == 0:
            response = self.node_stub0.get_request(request)
        elif stub == 1:
            response = self.node_stub1.get_request(request)
        else:
            response = self.node_stub2.get_request(request)

        x = list(response.values)
        #self.assertEqual(len(values), len(x), "len(values) != len(responses)")
        self.assertListEqual(values, x)

    def add_helper(self):
        # adds keys in node 0
        request = RN_pb2.NodeGetRequest(
            type=type_pb2.ADD, key="Sam", values=["14"])
        self.node_stub0.get_request(request)

        request = RN_pb2.NodeGetRequest(
            type=type_pb2.ADD, key="bob1", values=["34"])
        self.node_stub0.get_request(request)

        request = RN_pb2.NodeGetRequest(
            type=type_pb2.ADD, key="Nico", values=["54", "612"])
        self.node_stub0.get_request(request)

        request = RN_pb2.NodeGetRequest(
            type=type_pb2.ADD, key="Serwar", values=["54"])
        self.node_stub0.get_request(request)

    def del_helper(self):
        # deletes keys in each node
        request = RN_pb2.NodeGetRequest(type=type_pb2.DELETE, key="Sam")
        self.node_stub0.get_request(request)

        request = RN_pb2.NodeGetRequest(type=type_pb2.DELETE, key="bob1")
        self.node_stub1.get_request(request)

        request = RN_pb2.NodeGetRequest(type=type_pb2.DELETE, key="Nico")
        self.node_stub2.get_request(request)

        request = RN_pb2.NodeGetRequest(type=type_pb2.DELETE, key="Serwar")
        self.node_stub2.get_request(request)


if __name__ == '__main__':
    unittest.main()
