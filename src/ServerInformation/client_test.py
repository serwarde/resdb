import grpc
import time

import src.ServerInformation.ServerInformation_pb2 as SI_pb2
import src.ServerInformation.ServerInformation_pb2_grpc as SI_pb2_grpc


def test_add(stub):
    
    # Add new servers
    request = SI_pb2.AddRequest(type=SI_pb2.LOADBALANCER, name="LB1", ip_address = "192.168.0.1:55003")
    response = stub.add_(request)
    assert response.message == "Add was successfull"

    request = SI_pb2.AddRequest(type=SI_pb2.ROUTER, name="Router1", ip_address = "192.168.0.1:55004")
    response = stub.add_(request)
    assert response.message == "Add was successfull"

    request = SI_pb2.AddRequest(type=SI_pb2.NODE, name="Node1", ip_address = "192.168.0.1:55005")
    response = stub.add_(request)
    assert response.message == "Add was successfull"

    # Try to add the same servers again
    request = SI_pb2.AddRequest(type=SI_pb2.LOADBALANCER, name="LB1", ip_address = "192.168.0.1:55003")
    response = stub.add_(request)
    assert response.message == "Add was not successfull"
    
    request = SI_pb2.AddRequest(type=SI_pb2.ROUTER, name="Router1", ip_address = "192.168.0.1:55004")
    response = stub.add_(request)
    assert response.message == "Add was not successfull"
    
    request = SI_pb2.AddRequest(type=SI_pb2.NODE, name="Node1", ip_address = "192.168.0.1:55005")
    response = stub.add_(request)
    assert response.message == "Add was not successfull"

    # Try to add on none existing server types
    request = SI_pb2.AddRequest(type=4, name="Node1", ip_address = "192.168.0.1:55005")
    response = stub.add_(request)
    assert response.message == "Add was not successfull"

    request = SI_pb2.AddRequest(type=-1, name="Node1", ip_address = "192.168.0.1:55005")
    response = stub.add_(request)
    assert response.message == "Add was not successfull"

def test_get(stub):
    
    # Tries to get the ips from existing names
    request = SI_pb2.GetRequest(type=SI_pb2.LOADBALANCER, name="LB1")
    response = stub.get_(request)
    assert response.ip_address == "192.168.0.1:55003"

    request = SI_pb2.GetRequest(type=SI_pb2.ROUTER, name="Router1")
    response = stub.get_(request)
    assert response.ip_address == "192.168.0.1:55004"

    request = SI_pb2.GetRequest(type=SI_pb2.NODE, name="Node1")
    response = stub.get_(request)
    assert response.ip_address == "192.168.0.1:55005"

    # Tries to get the ips from non existing names
    request = SI_pb2.GetRequest(type=SI_pb2.LOADBALANCER, name="LB2")
    response = stub.get_(request)
    assert response.message == "No IP-Address for this Name found"
    
    request = SI_pb2.GetRequest(type=SI_pb2.ROUTER, name="Router2")
    response = stub.get_(request)
    assert response.message == "No IP-Address for this Name found"
    
    request = SI_pb2.GetRequest(type=SI_pb2.NODE, name="Node2")
    response = stub.get_(request)
    assert response.message == "No IP-Address for this Name found"

   # Tries to get the ips from existing names on wrong servers
    request = SI_pb2.GetRequest(type=4, name="Node1")
    response = stub.get_(request)
    assert response.message == "No IP-Address for this Name found"

    request = SI_pb2.GetRequest(type=-1, name="Node1")
    response = stub.get_(request)
    assert response.message == "No IP-Address for this Name found"

def test_get_random(stub):
    # Tries to get the a random server with one dict entry
    request = SI_pb2.GetRandomRequest(type=SI_pb2.LOADBALANCER)
    response = stub.get_random_(request)
    assert (response.name == "LB1" and response.ip_address == "192.168.0.1:55003")

    request = SI_pb2.GetRandomRequest(type=SI_pb2.ROUTER)
    response = stub.get_random_(request)
    assert response.name == "Router1" and response.ip_address == "192.168.0.1:55004"

    request = SI_pb2.GetRandomRequest(type=SI_pb2.NODE)
    response = stub.get_random_(request)
    assert response.name == "Node1" and response.ip_address == "192.168.0.1:55005"

    # Tries to get the a random server with multiple dict entries
    request = SI_pb2.AddRequest(type=SI_pb2.LOADBALANCER, name="LB2", ip_address="192.168.0.1:55004")
    response = stub.add_(request)
    request = SI_pb2.AddRequest(type=SI_pb2.LOADBALANCER, name="LB3", ip_address="192.168.0.1:55005")
    response = stub.add_(request)
    
    request = SI_pb2.GetRandomRequest(type=SI_pb2.LOADBALANCER)
    response = stub.get_random_(request)
    assert response.name in ["LB1", "LB2", "LB3"] and response.ip_address in ["192.168.0.1:55003", "192.168.0.1:55004", "192.168.0.1:55005"]
    response = stub.get_random_(request)
    assert response.name in ["LB1", "LB2", "LB3"] and response.ip_address in ["192.168.0.1:55003", "192.168.0.1:55004", "192.168.0.1:55005"]
    response = stub.get_random_(request)
    assert response.name in ["LB1", "LB2", "LB3"] and response.ip_address in ["192.168.0.1:55003", "192.168.0.1:55004", "192.168.0.1:55005"]

    # Tries to get the a random server with multiple on wrong type
    request = SI_pb2.GetRandomRequest(type=4)
    response = stub.get_random_(request)
    assert response.message == "No IP-Addresses are saved"

    request = SI_pb2.GetRandomRequest(type=-1)
    response = stub.get_random_(request)
    assert response.message == "No IP-Addresses are saved"

def test_get_all(stub):
    # Tries to get the a random server with one dict entry
    request = SI_pb2.GetAllRequest(type=SI_pb2.LOADBALANCER)
    responses = stub.get_all_(request)
    for i, response in enumerate(responses):
        if i == 0:
            assert response.ip_address == "192.168.0.1:55003" and response.name == "LB1"
        elif i == 1:
            assert response.ip_address == "192.168.0.1:55004" and response.name == "LB2"
        elif i == 2:
            assert response.ip_address == "192.168.0.1:55005" and response.name == "LB3"

def test_delete(stub):
    
    # trie to delete servers
    request = SI_pb2.DeleteRequest(type=SI_pb2.LOADBALANCER, name="LB1")
    response = stub.delete_(request)
    assert response.message == "Delete was successfull"

    request = SI_pb2.DeleteRequest(type=SI_pb2.ROUTER, name="Router1")
    response = stub.delete_(request)
    assert response.message == "Delete was successfull"

    request = SI_pb2.DeleteRequest(type=SI_pb2.NODE, name="Node1")
    response = stub.delete_(request)
    assert response.message == "Delete was successfull"

    # Try to delete the same servers again
    request = SI_pb2.DeleteRequest(type=SI_pb2.LOADBALANCER, name="LB1")
    response = stub.delete_(request)
    assert response.message == "Delete was not successfull"
    
    request = SI_pb2.DeleteRequest(type=SI_pb2.ROUTER, name="Router1")
    response = stub.delete_(request)
    assert response.message == "Delete was not successfull"
    
    request = SI_pb2.DeleteRequest(type=SI_pb2.NODE, name="Node1")
    response = stub.delete_(request)
    assert response.message == "Delete was not successfull"

    # Try to delete on none existing server types
    request = SI_pb2.DeleteRequest(type=4, name="Node1")
    response = stub.delete_(request)
    assert response.message == "Delete was not successfull"

    request = SI_pb2.DeleteRequest(type=-1, name="Node1")
    response = stub.delete_(request)
    assert response.message == "Delete was not successfull"

def test_delete_all(stub):
    # Delete all entries from the dicts
    request = SI_pb2.DeleteAllRequest(type=SI_pb2.LOADBALANCER)
    response = stub.delete_all_(request)
    assert response.message == "Delete was successfull"
    
    request = SI_pb2.DeleteAllRequest(type=SI_pb2.ROUTER)
    response = stub.delete_all_(request)
    assert response.message == "Delete was successfull"
    
    request = SI_pb2.DeleteAllRequest(type=SI_pb2.NODE)
    response = stub.delete_all_(request)
    assert response.message == "Delete was successfull"

    # try to delete all from an none existing server type
    request = SI_pb2.DeleteAllRequest(type=-1)
    response = stub.delete_all_(request)
    assert response.message == "Delete was not successfull"


if __name__ == '__main__':
    channel = grpc.insecure_channel('localhost:50050')
    stub = SI_pb2_grpc.ServerInformationStub(channel)

    test_delete_all(stub)
    test_add(stub)
    test_get(stub)
    test_get_random(stub)
    test_get_all(stub)
    test_delete(stub)

    print("Everything passed")
 