import grpc
import time

import src.Rendezvous.RendezvousNode_pb2 as RN_pb2
import src.Rendezvous.RendezvousNode_pb2_grpc as RN_pb2_grpc

import src.Rendezvous.RendezvousHashing_pb2 as RH_pb2
import src.Rendezvous.RendezvousHashing_pb2_grpc as RH_pb2_grpc

import src.Rendezvous.type_pb2 as type_pb2

import time
import unittest

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

    def test1_add_node(self):
        request = RH_pb2.RendezvousInformation(name="node0",ip_address="172.17.0.4:50251")
        self.router_stub.add_node(request)
        
        # adds some values to the first server
        self.add_helper()

        # adds two more nodes
        request = RH_pb2.RendezvousInformation(name="node1",ip_address="172.17.0.5:50252")
        self.router_stub.add_node(request)
        request = RH_pb2.RendezvousInformation(name="node2",ip_address="172.17.0.6:50253")
        self.router_stub.add_node(request)

        # check if the values got redistributed
        self.tst_value_for_key("Sam",["14"])
        self.tst_value_for_key("bob1",["34"],1)
        self.tst_value_for_key("Nico",["54", "612"],2)
        self.tst_value_for_key("Serwar",["54"],2)

        # deletes the values
        self.del_helper()

    def test2_find_responsible_node(self):
        # add KV for Sam. Sam is saved at Node0
        request = RH_pb2.RendezvousFindNodeRequest(type=type_pb2.ADD,key="Sam",value="14")
        self.router_stub.forward_to_responsible_node(request)
        self.tst_value_for_key("Sam",["14"])

        # add KV for Sam. Sam is saved at Node0
        request = RH_pb2.RendezvousFindNodeRequest(type=type_pb2.DELETE,key="Sam",value="14")
        self.router_stub.forward_to_responsible_node(request)
        self.tst_value_for_key("Sam",[])

        # add KV for bob1. bob1 is saved at Node1
        request = RH_pb2.RendezvousFindNodeRequest(type=type_pb2.ADD,key="bob1",value="14")
        self.router_stub.forward_to_responsible_node(request)
        self.tst_value_for_key("bob1",["14"],1)

        # add KV for bob1. bob1 is saved at Node1
        request = RH_pb2.RendezvousFindNodeRequest(type=type_pb2.DELETE,key="bob1",value="14")
        self.router_stub.forward_to_responsible_node(request)
        self.tst_value_for_key("bob1",[],1)

        # add KV for Nico. Nico is saved at Node2
        request = RH_pb2.RendezvousFindNodeRequest(type=type_pb2.ADD,key="Nico",value="14")
        self.router_stub.forward_to_responsible_node(request)
        self.tst_value_for_key("Nico",["14"],2)

        # add KV for Nico. Nico is saved at Node2
        request = RH_pb2.RendezvousFindNodeRequest(type=type_pb2.DELETE,key="Nico",value="14")
        self.router_stub.forward_to_responsible_node(request)
        self.tst_value_for_key("Nico",[],2)

    def test3_remove_node(self):
        pass

    def tst_value_for_key(self, key, values, stub=0):

        request = RN_pb2.NodeGetRequest(type=type_pb2.GET,key=key)
        if stub==0:
            responses = self.node_stub0.get_request(request)
        elif stub == 1:
            responses = self.node_stub1.get_request(request)
        else:
            responses = self.node_stub2.get_request(request)
        
        x = []
        for response in responses:
            x.append(response.value)
        
        self.assertEqual(len(values), len(x), "len(values) != len(responses)")
        self.assertListEqual(values, x)    


    def add_helper(self):
        # adds keys in node 0
        request = RN_pb2.NodeGetRequest(type=type_pb2.ADD,key="Sam",value="14")
        responses = self.node_stub0.get_request(request)
        for i in responses:
            pass
        request = RN_pb2.NodeGetRequest(type=type_pb2.ADD,key="bob1",value="34")
        responses = self.node_stub0.get_request(request)
        for i in responses:
            pass
        request = RN_pb2.NodeGetRequest(type=type_pb2.ADD,key="Nico",value="54")
        responses = self.node_stub0.get_request(request)
        for i in responses:
            pass
        request = RN_pb2.NodeGetRequest(type=type_pb2.ADD,key="Nico",value="612")
        responses = self.node_stub0.get_request(request)
        for i in responses:
            pass
        request = RN_pb2.NodeGetRequest(type=type_pb2.ADD,key="Serwar",value="54")
        responses = self.node_stub0.get_request(request)
        for i in responses:
            pass

    def del_helper(self):
        # deletes keys in each node
        request = RN_pb2.NodeGetRequest(type=type_pb2.DELETE,key="Sam")
        responses = self.node_stub0.get_request(request)
        for i in responses:
            pass
        
        request = RN_pb2.NodeGetRequest(type=type_pb2.DELETE,key="bob1")
        responses = self.node_stub1.get_request(request)
        for i in responses:
            pass

        request = RN_pb2.NodeGetRequest(type=type_pb2.DELETE,key="Nico")
        responses = self.node_stub2.get_request(request)
        for i in responses:
            pass

        request = RN_pb2.NodeGetRequest(type=type_pb2.DELETE,key="Serwar")
        responses = self.node_stub2.get_request(request)
        for i in responses:
            pass

if __name__ == '__main__':
    unittest.main()
