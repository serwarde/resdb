from abc import abstractmethod
from better_abc import ABCMeta, abstract_attribute
from typing import Union

class AbstractNodeClass(metaclass=ABCMeta):
    
    _host_name = abstract_attribute()
    _host_ip = abstract_attribute()
    _http_port = abstract_attribute()
    _objects = abstract_attribute()
    
    def get_host_name(self):
        return self._host_name
    
    def get_host_ip(self):
        return self._host_name
    
    def get_host_port(self):
        return self._host_name

    @abstractmethod
    def add_object(self, key, value):
        pass
    
    @abstractmethod
    def remove_object(self, key, value=None):
        pass
    
    @abstractmethod
    def update_object(self, key, value):
        pass
    
    @abstractmethod
    def get_object(self, key) -> Union[int,str,list,bool,tuple,dict]:
        pass
    
    def get_request(self, type, key, value):
        if type == "add":
            self.add_object(key,value)
        elif type == "remove":
            self.remove_object(key,value)
        elif type == "get":
            self.get_object(key)
        elif type == "update":
            self.update_object(key,value)
            
    