from abc import abstractmethod
from better_abc import ABCMeta, abstract_attribute

class AbstractRouterClass(metaclass=ABCMeta):
    @abstractmethod
    def add_node(self, node):
        pass
    
    @abstractmethod
    def remove_node(self, node):
        pass
    
    @abstractmethod
    def find_responsible_node(self, key):
        # returns node id
        pass
    
    