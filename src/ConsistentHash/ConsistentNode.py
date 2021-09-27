# from Node.node_abstract import AbstractNodeClass
from typing import DefaultDict, Union
from collections import defaultdict
import hashlib
import random
import time
from concurrent import futures
import grpc
import ConsistentHashing_pb2 as pb2
import ConsistentHashing_pb2_grpc as pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class ConsistentNode(pb2_grpc.ConsistentHashingServicer):

    def __init__(self, name='444', ip_adress='localhost', port='90001',
                 CH=ConsistentHashing([node1, node2, node3, node4])):
        self._host_name = name
        self.CH = CH
        self._host_ip = ip_adress
        self._http_port = port
        self._objects_dict = defaultdict(lambda: [])
        self._objects_dict['ff'] = 'aaa'
        # TODO: incomplete
        self._replication_dict = defaultdict(lambda: [])
        self._replication_dict['90001'] = {}
        self._replication_dict['90001']['ff'] = 'data2'
        self.replication_num = 1

    def hash_value_for_key(self, key):
        # implement a hash function
        m = hashlib.md5()
        m.update(key.encode('utf-8'))
        return m.hexdigest()

    def add_object(self, key, value):
        """
        adds a new object to the dict
        key = the key for the object
        value = value of the key
        """
        # self._objects_dict[key] = self._objects_dict[key].append(value)

        self._objects_dict[key] = value

    def remove_object(self, key):
        """
        removes an object from the dict,
        if a value is given it just removes the value/s for the key

        key = the key for the object
        value = optional parameter, if a specific value/s should be deleted
        """
        if key in self._objects_dict:
            del self._objects_dict[key]

    def get_object(self, key) -> Union[int, str, list, bool, tuple, dict]:
        """
        returns the values for a given key
        key = the key for the object
        """
        return self._objects_dict[key]

    def get_all_object(self):
        return self._objects_dict

    def send_request(self, request, context, node):
        print(request)
        print(node)
        channel = grpc.insecure_channel(node.ip_adress + ':' + node.port)
        stub = pb2_grpc.ConsistentHashingStub(channel)
        request = pb2.ConsistentFindNodeRequest(key=request.key, NodeIp=node.ip_adress, RequestType=request.RequestType,
                                                ClientIp='444')
        response = stub.send_request(request)
        print(response)

    # find a coresponding node to replicate
    def find_replication(self, preferrence_list, coordinator):
        position = preferrence_list.index(coordinator)
        #         print('position',position)

        if (len(preferrence_list) - (position + 1)) >= self.replication_num:
            return preferrence_list[position + 1: position + self.replication_num + 1]
        else:
            return preferrence_list[position - self.replication_num: position]

    def update_coordinator(self):
        for key in self._objects_dict.keys():
            preferrence_list, _ = self.CH.find_preference_list(key)
            coordinator = node2
            while coordinator._http_port == self._http_port:
                coordinator = random.sample(preferrence_list, 1)[0]

            print('upadate coordinator', coordinator._http_port)
            print([node._http_port for node in preferrence_list])
            for node in preferrence_list:
                channel = grpc.insecure_channel('localhost' + ":" + node._http_port)
                stub = pb2_grpc.ConsistentHashingStub(channel)

                request = pb2.GeneralRequest(key=key, NodeIp=request.NodeIp, NodePort=request.NodePort,
                                             RequestType='update coordinator',
                                             ClientIp=request.ClientIp, CoordinatorIp=request.CoordinatorIp,
                                             value=request.value,
                                             oldIp=self._http_port, newIp=coordinator._http_port)

                #                 request = pb2.GeneralRequest(key=key, NodeIp=request.NodeIp, NodePort=request.NodePort,ClientIp=request.ClientIp,
                #                                              oldIp=self._http_port, newIp =coordinator._http_port, RequestType='update coordinator') ######################################
                response = stub.get_request(request)

    def update_replication(self):
        for key in self._replication_dict.keys():
            preferrence_list, _ = self.CH.find_preference_list(key)
            last_node = preferrence_list[-1]

            hashcode = self.CH.get_hash(last_node._host_name + '#' + str(0))
            position = self.CH._sorted_hashcode.index(hashcode)

            if position != len(self.CH._sorted_hashcode):
                new_come_node = self.CH.ring[self.CH._sorted_hashcode[position + 1]]
            else:
                new_come_node = self.CH.ring[self.CH._sorted_hashcode[0]]

            channel = grpc.insecure_channel('local' + ":" + new_come_node._http_port)
            stub = pb2_grpc.ConsistentHashingStub(channel)
            request = pb2.GeneralRequest(key=request.key, NodeIp=request.NodeIp, NodePort=request.NodePort,
                                         ##########################request 有问题
                                         RequestType='replicaion',
                                         ClientIp=request.ClientIp, CoordinatorIp=key)
            response = stub.get_request(request)

    def get_request(self, request, context):
        """
        GRPC

        Node gets a request, checks the type of the request and calls the responsible function
        type = can be (get, add, remove or update)
        key = the key for the item that should be stored
        value = only necessary for add and update
        """
        key = request.key
        preferrence_list, _ = self.CH.find_preference_list(key)
        hostname_list = [node._host_name for node in preferrence_list]
        coordinator = random.sample(preferrence_list, 1)[0]

        object_request_list = ['add_object', 'get_object', 'remove_object', 'replicaion', 'find_preferrence_list']
        node_request_list = ['add_node', 'remove_node', 'update coordinator', 'update hashring']

        print('received request:', request.RequestType)

        # if node._host_name == self._host_name:
        if request.RequestType in object_request_list:
            if request.RequestType == 'add_object':
                # TODO incomplete
                if self._host_name in hostname_list:  ###############################
                    self.add_object(request.key, request.value)
                    replication = self.find_replication(preferrence_list, coordinator)
                    print(replication, '1111')

                    #                     return pb2.SimpleReply(message="Successfull")####
                    for re in replication:
                        print('replication port', re._host_name, re._http_port)
                        channel = grpc.insecure_channel('localhost' + ":" + '90001')  #################################
                        stub = pb2_grpc.ConsistentHashingStub(channel)
                        request = pb2.GeneralRequest(key=request.key, NodeIp=request.NodeIp, NodePort=request.NodePort,
                                                     RequestType='replicaion',
                                                     ClientIp=request.ClientIp, CoordinatorIp=self._http_port,
                                                     value=request.value)
                        #                         print(request)
                        response = stub.get_request(request)
                        print(response)
                        # send_request()# send request to the node and store the replication
                else:
                    # send_Request(coordinator, request)
                    channel = grpc.insecure_channel('localhost' + ":" + coordinator._http_port)
                    stub = pb2_grpc.ConsistentHashingStub(channel)
                    request = pb2.GeneralRequest(key=request.key, NodeIp=request.NodeIp, NodePort=request.NodePort,
                                                 RequestType=request.RequestType, ClientIp=request.ClientIp,
                                                 CoordinatorIp=self._http_port, value=request.value)  # 测试
                    response = stub.get_request(request)
                return pb2.SimpleReply(message="Successfull")


            elif request.RequestType == 'get_object':

                # TODO read n nodes, w + r > n
                # n = 0
                # for node in preferrence_list:
                #     if n <= self.CH.preference_list_num - self.replication_num +1:
                #         n += 1
                #         channel = grpc.insecure_channel(node._host_ip + ":" + node._http_port)
                #         stub = pb2_grpc.ConsistentHashingStub(channel)
                #         request = pb2.GeneralRequest(key=request.key, NodeIp=request.NodeIp, NodePort=request.NodePort,
                #                                      RequestType=request.RequestType, ClientIp=request.ClientIp,
                #                                      CoordinatorIp=coordinator._host_ip)  # 测试
                #         response = stub.get_request(request)
                #
                #

                res = []
                n = 0
                for node in preferrence_list:
                    if n <= self.CH.preference_list_num - self.replication_num + 1:
                        n += 1
                        channel = grpc.insecure_channel(node._host_ip + ":" + node._http_port)
                        stub = pb2_grpc.ConsistentHashingStub(channel)
                        request = pb2.GeneralRequest(key=request.key, NodeIp=request.NodeIp, NodePort=request.NodePort,
                                                     RequestType=request.RequestType, ClientIp=request.ClientIp,
                                                     CoordinatorIp='xxx')
                        response = stub.get_request(request)
                        res.append(response)



            elif request.RequestType == 'remove_object':
                # TODO
                for node in preferrence_list:
                    channel = grpc.insecure_channel(node._host_ip + ":" + node._http_port)
                    stub = pb2_grpc.ConsistentHashingStub(channel)
                    request = pb2.GeneralRequest(key=request.key, NodeIp=request.NodeIp, NodePort=request.NodePort,
                                                 RequestType=request.RequestType, ClientIp=request.ClientIp,
                                                 CoordinatorIp='xxx')
                    response = stub.get_request(request)
                return pb2.SimpleReply(message="Remove object Successfull")

            # data replicate in replication_dict
            elif request.RequestType == 'replicaion':
                # TODO
                self._replication_dict[request.CoordinatorIp] = {}
                self._replication_dict[request.CoordinatorIp][request.key] = request.value
                return pb2.SimpleReply(message="Replication Successfull")

        if request.RequestType in node_request_list:  #########
            # TODO After adding the new node,
            """ 1.If the node that contains the replication is still in the Preference List: 
                redistribute, update the Preference List.
                2.If the node that contains the replication is not in the Preference List:
                redistribute, update the Preference List, send replication to the new node,
                delete replication from the old node.
            """
            if request.RequestType == 'add_node':
                # node = Node(request.NodeName, request.NodeIp, request.NodePort)
                self.CH.redistribute_objects_for_add(node)
                if request.count <= 4:
                    brodcast(self, self.CH, request)
                self.CH.add_node(node)
                return pb2.SimpleReply(message="add node Successfull")


            elif request.RequestType == 'update coordinator':
                self._replication_dict[request.newIp] = self._replication_dict[
                    request.oldIp]  ######################## new old
                del self._replication_dict[request.oldIp]
                return pb2.SimpleReply(message="2 update coordinator Successfull")

            # update hash ring after remove a node
            elif request.RequestType == 'update hashring':
                for hashcode, node in self.CH.ring.items():
                    if node._http_port == request.removedNode:
                        del self.CH.ring[hashcode]
                        return pb2.SimpleReply(message="update hashring Successfull")



            """ 5 step to remove a node with replication
            1.update coordinator for coresponding data that stored in node
            2.update replication node 
            3.redistribute a part of hasing ring 
            4.broadcast information that this node has been removed to any other node in consistent hash ring
            5.removed node from hash ring
            """
            elif request.RequestType == 'remove_node':

            # update coordinator
            for key in self._objects_dict.keys():

                preferrence_list, _ = self.CH.find_preference_list(key)
                coordinator = node2
                while coordinator._http_port == self._http_port:
                    coordinator = random.sample(preferrence_list, 1)[0]


                for node in preferrence_list:
                    if node._http_port != self._http_port:
                        channel = grpc.insecure_channel('localhost' + ":" + node._http_port)
                        stub = pb2_grpc.ConsistentHashingStub(channel)

                        request = pb2.GeneralRequest(key=key, NodeIp=request.NodeIp, NodePort=request.NodePort,
                                                     RequestType='update coordinator',
                                                     ClientIp=request.ClientIp, CoordinatorIp=request.CoordinatorIp,
                                                     value=request.value,
                                                     oldIp=self._http_port, newIp=coordinator._http_port)

                        response = stub.get_request(request)
                        print(response)

            #  update replication node
            for coordinator_ip in self._replication_dict.keys():

                for key, value in self._replication_dict[coordinator_ip]:
                    preferrence_list, _ = self.CH.find_preference_list(key)
                    last_node = preferrence_list[-1]

                    hashcode = self.CH.get_hash(last_node._host_name + '#' + str(0))
                    position = self.CH._sorted_hashcode.index(hashcode)

                    if position != len(self.CH._sorted_hashcode) - 1:
                        new_come_node = self.CH.ring[self.CH._sorted_hashcode[position + 1]]
                    else:
                        new_come_node = self.CH.ring[self.CH._sorted_hashcode[0]]

                    #                         print('old preferrence_list',[node._http_port for node in preferrence_list])
                    #                         print('new_come_node._http_port',new_come_node._http_port)

                    channel = grpc.insecure_channel('localhost' + ":" + new_come_node._http_port)
                    stub = pb2_grpc.ConsistentHashingStub(channel)
                    request = pb2.GeneralRequest(key=key, NodeIp=request.NodeIp, NodePort=request.NodePort,
                                                 RequestType='replicaion', value=value,
                                                 ClientIp=request.ClientIp, CoordinatorIp=coordinator_ip)
                    response = stub.get_request(request)

            # redistribute a part of hasing ring
            for hashcode, node in self.CH.ring.items():
                if node._http_port == self._http_port:
                    self.CH.redistribute_objects_for_remove(node)

            # broadcast information to any other node in hash ring
            for hashcode, node in self.CH.ring.items():
                if node._http_port != self._http_port:
                    #                         print('update ring',node._http_port)
                    channel = grpc.insecure_channel('localhost' + ":" + node._http_port)
                    stub = pb2_grpc.ConsistentHashingStub(channel)
                    request = pb2.GeneralRequest(key=request.key, NodeIp=request.NodeIp, NodePort=request.NodePort,
                                                 RequestType='update hashring', value=request.value,
                                                 ClientIp=request.ClientIp, CoordinatorIp='00000',
                                                 removedNode=self._http_port)
                    response = stub.get_request(request)
                    print(response)

            return pb2.SimpleReply(message="remode node Successfull")


