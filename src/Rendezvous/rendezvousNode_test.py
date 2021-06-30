import grpc
import time

import src.Rendezvous.RendezvousNode_pb2 as RN_pb2
import src.Rendezvous.RendezvousNode_pb2_grpc as RN_pb2_grpc
import time
import unittest

class TestRendezvousNodeMethods(unittest.TestCase):
    def __init__(self, *args, **kwargs):
            super(TestRendezvousNodeMethods, self).__init__(*args, **kwargs)
            channel = grpc.insecure_channel('localhost:50250')
            self.stub = RN_pb2_grpc.RendezvousNodeStub(channel)

    def test1_hash(self):
        # Get Hash values for diffrent keys
        request = RN_pb2.NodeHashValueForRequest(key="Sam")
        response = self.stub.hash_value_for_key(request)
        self.assertEqual(response.hashValue, 1.9765778094468415e+38)

        request = RN_pb2.NodeHashValueForRequest(key="Nico")
        response = self.stub.hash_value_for_key(request)
        self.assertEqual(response.hashValue, 2.7165206766072618e+38)
        
        request = RN_pb2.NodeHashValueForRequest(key="Serwar")
        response = self.stub.hash_value_for_key(request)
        self.assertEqual(response.hashValue, 5.394662572114302e+37)

        request = RN_pb2.NodeHashValueForRequest(key="Shan")
        response = self.stub.hash_value_for_key(request)
        self.assertEqual(response.hashValue, 1.850626479697317e+38)

        request = RN_pb2.NodeHashValueForRequest(key="Zhanglei")
        response = self.stub.hash_value_for_key(request)
        self.assertEqual(response.hashValue, 1.604904174640645e+38)

    # TODO: adding does only work when we loop over the responses. if we don't nothing is done
    # TODO: look into why this is the case
    def test2_add(self):
        # add entries to the dict
        request = RN_pb2.NodeGetRequest(type=RN_pb2.ADD,key="Sam",value="24")
        responses = self.stub.get_request(request)

        for i in responses:
            pass

        request = RN_pb2.NodeGetRequest(type=RN_pb2.ADD,key="Sam",value="14")
        responses = self.stub.get_request(request)

        for i in responses:
            pass

        request = RN_pb2.NodeGetRequest(type=RN_pb2.ADD,key="Sam",value="42")
        responses = self.stub.get_request(request)

        for i in responses:
            pass

        request = RN_pb2.NodeGetRequest(type=RN_pb2.GET,key="Sam")
        responses = self.stub.get_request(request)

        x = []
        for i in responses:
            x.append(i.value)
        print(x)

    def test3_add(self):
        # add entries to the dict
        request = RN_pb2.NodeGetRequest(type=RN_pb2.ADD,key="Sam",value="24")
        responses = self.stub.get_request(request)

        request = RN_pb2.NodeGetRequest(type=RN_pb2.ADD,key="Sam",value="14")
        responses = self.stub.get_request(request)

        request = RN_pb2.NodeGetRequest(type=RN_pb2.ADD,key="Sam",value="42")
        responses = self.stub.get_request(request)

        request = RN_pb2.NodeGetRequest(type=RN_pb2.GET,key="Sam")
        responses = self.stub.get_request(request)

        x = []
        for i in responses:
            x.append(i.value)
        print(x)


        
    def tst3_delete(self):
        request = RN_pb2.NodeGetRequest(type=RN_pb2.GET,key="Sam")
        responses = self.stub.get_request(request)
        
        self.get_test("Sam", ["24", "5", "42"])

        # Delete one entrie 
        request = RN_pb2.NodeGetRequest(type=RN_pb2.DELETE,key="Sam",value="24")
        response = self.stub.get_request(request)
        
        #self.get_test("Sam", ["42", "5"])

        # Delete All
        request = RN_pb2.NodeGetRequest(type=RN_pb2.DELETE,key="Sam")
        response = self.stub.get_request(request)

        request = RN_pb2.NodeGetRequest(type=RN_pb2.GET,key="Sam")
        responses = self.stub.get_request(request)

        i = 0
        for _ in responses:
            i += 1
        
        self.assertEqual(i,0, "Delete all did not work correct")

    def get_test(self, key, values):

        request = RN_pb2.NodeGetRequest(type=RN_pb2.GET,key=key)
        responses = self.stub.get_request(request)
        j = 0
        x = []
        for response in responses:
            x.append(response.value)
            j += 1
        print(x)

        self.assertEqual(len(values), j, "len(values) != len(responses)")


       

    

if __name__ == '__main__':
    unittest.main()
