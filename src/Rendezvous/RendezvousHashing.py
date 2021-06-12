from Rendezvous.RendezvousNode import RendezvousNode
from Routing.router_abstract import AbstractRouterClass

class RendezvousHashing(AbstractRouterClass):
    ## TODO: Locking this attribute to ensure sync
    _list_of_nodes = []

    def add_node(self, node):
        """
        adds a new Node into the Router.
        Also handles node balancing

        node: the node that should be added
        """
        self._list_of_nodes.append(node)
        self.redistribute_objects_to_new_node(node)

    def remove_node(self, node):
        """
        removes a Node from the Router.
        Also handles node balancing

        node: the node that should be deleted
        """
        self._list_of_nodes.remove(node)
        self.redistribute_objects_from_deleted_node(node)

    def find_responsible_node(self, key) -> RendezvousNode:
        """
        finds the responsible node, for a given key

        key: the key of which we want to know the node

        return the Node for the given key
        """
        champion = None
        maxValue = -1
        for node in self._list_of_nodes:
            currentValue = node.hash_value_for_key(key)
            if currentValue > maxValue:
                maxValue = currentValue
                champion = node
        return champion

    def redistribute_objects_from_deleted_node(self, node):
        """
        Restributes all Key,Values of a deleted Node

        node: the node that should be deleted
        """
        for k,v in node.get_objects().items():
            self.find_responsible_node(k,v).add_object(k,v)
    
    def redistribute_objects_to_new_node(self, node):
        """
        Restributes all Key,Values of a all Nodes, if the new node is the champion

        node: the node that will be added
        """
        temp_list_of_nodes = self._list_of_node
        temp_list_of_nodes.remove(node)
        #TODO: threading?
        for n in temp_list_of_nodes:
            n.send_item_to_new_node(node)