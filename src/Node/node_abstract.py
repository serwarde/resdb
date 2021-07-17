from abc import abstractmethod
from better_abc import ABCMeta, abstract_attribute
from typing import Union

class AbstractNodeClass(metaclass=ABCMeta):
    
    _host_name = abstract_attribute()
    _host_ip = abstract_attribute()
    _http_port = abstract_attribute()
    _objects_dict = abstract_attribute()
    
    def get_host_name(self):
        """
        Returns the host_name of the node
        """
        return self._host_name
    
    def get_host_ip(self):
        """
        Returns the host_ip of the node
        """
        return self._host_name
    
    def get_host_port(self):
        """
        Returns the host_port of the node
        """
        return self._host_name

    @abstractmethod
    def hash_value_for_key(self, key):
        """
        Returns the hash value of a given key
        """
        pass

    @abstractmethod
    def add_object(self, key, value):
        """
        adds a new object to the dict
        
        TODO: What happens if the key is already inside
        
        key = the key from the object
        value = value of the key
        """
        pass
    
    @abstractmethod
    def remove_object(self, key, value=None):
        """
        removes a object from the dict, 
        if a value is given it just removes the value/s for the key
        
        TODO: What happens if the key is not in the list / the value is not in the list
        
        key = the key from the object
        value = optional parameter, if a specific value/s should be deleted
        """
        pass
    
    @abstractmethod
    def get_object(self, key) -> Union[int,str,list,bool,tuple,dict]:
        """
        returns the values for a given key
        
        key = the key from the object
        """
        pass

    def get_objects(self) -> dict:
        """
        returns all objects in node
        """
        return self._objects_dict
    
    def get_request(self, type, key, value):
        """
        Node gets a request, checks the type of the request and calls the responsible function
        
        type = can be (get, add, remove or update)
        key = the key for the item that should be stored
        value = only necessary for add and update
        """
        if type == "add":
            self.add_object(key,value)
        elif type == "remove":
            self.remove_object(key,value)
        elif type == "get":
            self.get_object(key)
            