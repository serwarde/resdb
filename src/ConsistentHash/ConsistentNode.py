# from Node.node_abstract import AbstractNodeClass
from typing import DefaultDict, Union
from collections import defaultdict
import hashlib


class ConsistentNode():

    def __init__(self, name='111', ip_adress='222', port='333'):
        self._host_name = name
        self._host_ip = ip_adress
        self._http_port = port
        # TODO: incomplete
        self._objects_dict = defaultdict(lambda: [])

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

    def remove_object(self, key, value=None):
        """
        removes an object from the dict,
        if a value is given it just removes the value/s for the key

        key = the key for the object
        value = optional parameter, if a specific value/s should be deleted
        """
        if key in self._objects_dict:
            if value:
                #                 self._objects_dict[key] = self._objects_dict[key].remove(value)
                del self._objects_dict[key]

            else:
                del self._objects_dict[key]

    def get_object(self, key) -> Union[int, str, list, bool, tuple, dict]:
        """
        returns the values for a given key
        key = the key for the object
        """
        return self._objects_dict[key]

    def get_all_object(self):
        return self._objects_dict