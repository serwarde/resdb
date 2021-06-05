from Node.node_abstract import AbstractNodeClass
from typing import DefaultDict, Union
from collections import defaultdict

class RendezvousNode(AbstractNodeClass):

    _node_weight = -1
    _node_seed = -1

    def __init__(self, name, ip_adress, port, weight):
        self._host_name = name
        self._host_ip = ip_adress
        self._http_port = port
        self._node_weight = weight
        # TODO: Check if ip_adress is a adequate seed for the node
        self._node_seed = ip_adress
        # TODO: Check if a list is a good representation for values
        self._objects_dict = defaultdict([])


    def hash_value_for_key(self, key):
        # TODO: Research and implement a hash function
        return -1

    def send_item_to_new_node(self, node):
        for k,v in self._objects_dict.items():
            if node.hash_value_for_key(k) >= self.hash_value_for_key(k):
                node.add_object(k,v)
                # TODO: maybe store hash values of the keys?

    def add_object(self, key, value):
        """
        adds a new object to the dict
        key = the key from the object
        value = value of the key

        TODO: extend to working with dicts as values
        """

        # using default dicts to ensure the possibility of adding multiple values
        self._objects_dict[key] = self._objects_dict[key].append(value)

    def remove_object(self, key, value=None):
        """
        removes a object from the dict, 
        if a value is given it just removes the value/s for the key
        
        key = the key from the object
        value = optional parameter, if a specific value/s should be deleted
        """
        if key in self._objects_dict:
            if value:
                self._objects_dict[key] = self._objects_dict[key].remove(value)
            else:
                del self._objects_dict[key]

    
    def update_object(self, key, value):
        """
        updates a object in the dict, 
        if a dict, list or tuple is used we append the value/s to the key
        key = the key from the object
        value = value of the key

        TODO: Check if necessary if we keep using lists as values in the defaultdict
        """

        self._objects_dict[key] = self._objects_dict[key].append(value)
    
    def get_object(self, key) -> Union[int,str,list,bool,tuple,dict]:
        """
        returns the values for a given key
        key = the key from the object
        """
        return self._objects_dict[key]