from abc import abstractmethod
from better_abc import ABCMeta, abstract_attribute

class AbstractRouterClass(metaclass=ABCMeta):
    @abstractmethod
    def add_node(self, node):
        """
        adds a new Node into the Router.
        Also handles node balancing
        """
        pass
    
    @abstractmethod
    def remove_node(self, node):
        """
        removes a new Node from the Router.
        Also handles node balancing
        """
        pass
    
    @abstractmethod
    def find_responsible_node(self, key):
        """
        finds the responsible node, for a given key
        """
        pass
    
    
