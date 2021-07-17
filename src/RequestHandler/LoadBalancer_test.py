'''
This is not a unit test, just a mocking of a real-case request from a user

'''

import LoadBalancer

if __name__ == '__main__':
    # TODO: does not work like that, just use tp_pb2.ADD or smth similiar
    loadBalancer = LoadBalancer()
    loadBalancer.request(1,key="Serwar",value="666")
    loadBalancer.request(1,key="Nico",value="666")
    loadBalancer.request(1,key="Sam",value="666")
    loadBalancer.request(2,key="Serwar",value="666")
    loadBalancer.request(2,key="Nico",value="666")
    loadBalancer.request(2,key="Sam",value="666")
    loadBalancer.request(3,key="Serwar",value="666")
    loadBalancer.request(3,key="Nico",value="666")
    loadBalancer.request(3,key="Sam",value="666")