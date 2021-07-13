import grpc
import time

import src.Rendezvous.RendezvousNode_pb2 as RN_pb2
import src.Rendezvous.RendezvousNode_pb2_grpc as RN_pb2_grpc
import time
import unittest

class TestRendezvousNodeMethods(unittest.TestCase):
    def __init__(self, *args, **kwargs):
            super(TestRendezvousNodeMethods, self).__init__(*args, **kwargs)
            channel = grpc.insecure_channel('localhost:50151')
            self.stub = RN_pb2_grpc.RendezvousNodeStub(channel)

    def test1_find_responsible_node(self):
        pass

    def test2_add_node(self):
        pass

    def test3_remove_node(self):
        pass


    """def test5_delete_all(self):
        # delete all for sam
        request = RN_pb2.NodeGetRequest(type=RN_pb2.DELETE,key="Sam")
        responses = self.stub.get_request(request)
        for i in responses:
            pass
        self.tst_value_for_key("Sam", [])

        # delete all for sand
        request = RN_pb2.NodeGetRequest(type=RN_pb2.DELETE,key="Sand")
        responses = self.stub.get_request(request)
        for i in responses:
            pass
        self.tst_value_for_key("Sand", [])

        # delete all for nico
        request = RN_pb2.NodeGetRequest(type=RN_pb2.DELETE,key="Nico")
        responses = self.stub2.get_request(request)
        for i in responses:
            pass
        self.tst_value_for_key("Nico", [])

        # delete all for Serwar
        request = RN_pb2.NodeGetRequest(type=RN_pb2.DELETE,key="Serwar")
        responses = self.stub2.get_request(request)
        for i in responses:
            pass
        self.tst_value_for_key("Serwar", [])

    def tst_value_for_key(self, key, values, stub=0):

        request = RN_pb2.NodeGetRequest(type=RN_pb2.GET,key=key)
        if stub==0:
            responses = self.stub.get_request(request)
        else:
            responses = self.stub2.get_request(request)
        
        x = []
        for response in responses:
            x.append(response.value)
        
        self.assertEqual(len(values), len(x), "len(values) != len(responses)")
        self.assertListEqual(values, x)    """

if __name__ == '__main__':
    unittest.main()
