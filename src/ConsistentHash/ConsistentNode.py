from Node.node_abstract import AbstractNodeClass
from typing import DefaultDict, Union
from collections import defaultdict
import hashlib

class ConsistentNode(AbstractNodeClass):

    def __init__(self, name, ip_adress, port):
        self._host_name = name
        self._host_ip = ip_adress
        self._http_port = port
        # TODO: incomplete
        self._objects_dict = defaultdict([])

    def get_hash(self, key):
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

        self._objects_dict[key] = self._objects_dict[key].append(value)

    def remove_object(self, key, value=None):
        """
        removes an object from the dict,
        if a value is given it just removes the value/s for the key

        key = the key for the object
        value = optional parameter, if a specific value/s should be deleted
        """
        if key in self._objects_dict:
            if value:
                self._objects_dict[key] = self._objects_dict[key].remove(value)
            else:
                del self._objects_dict[key]


    def get_object(self, key) -> Union[int, str, list, bool, tuple, dict]:
        """
        returns the values for a given key
        key = the key for the object
        """
        return self._objects_dict[key]
