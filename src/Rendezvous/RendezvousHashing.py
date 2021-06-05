from Rendezvous.RendezvousNode import RendezvousNode
from Routing.router_abstract import AbstractRouterClass

class RendezvousHashing(AbstractRouterClass):
    ## TODO: Locking this attribute to ensure sync
    _list_of_nodes = []

    def add_node(self, node):
        self._list_of_nodes.append(node)
        self.redistribute_objects(node)

    def remove_node(self, node):
        self._list_of_nodes.remove(node)
        self.redistribute_objects_from_deleted_object(node)

    def find_responsible_node(self, key):
        champion = None
        maxValue = -1
        for node in self._list_of_nodes:
            currentValue = node.hashFunction(key)
            if currentValue > maxValue:
                maxValue = currentValue
                champion = node
        return champion

    def redistribute_objects_from_deleted_object(self, node):
        for k,v in node.get_objects().items():
            self.find_responsible_node(k,v).add_object(k,v)
    
    def redistribute_objects_to_new_object(self, node):
        temp_list_of_nodes = self._list_of_node
        temp_list_of_nodes.remove(node)
        #TODO: threading?
        for n in temp_list_of_nodes:
            n.sendItemToNewNode(node)