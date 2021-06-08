from Consistent.ConsistentNode import ConsistentNode
from Routing.router_abstract import AbstractRouterClass
import hashlib


class ConsistentHashing(AbstractRouterClass):

    def __init__(self, nodes=None, virtual_copies= 10):
        """
        initialize
        """
        self.virtual_copies = virtual_copies
        self.ring = dict()
        self._sorted_keys = []

        if nodes:
            for node in nodes:
                self.add_node(node)

    def add_node(self, node):
        """
        Add a new node and its virtual nodes into the hash ring
        """
        for i in range(self.virtual_copies):
            virtual_node = f"{node}#{i}"
            key = self.get_hash(virtual_node)
            self.ring[key] = node
            self._sorted_keys.append(key)

        self._sorted_keys.sort()
        self.redistribute_objects(node)


    def remove_node(self, node):
        """
        Remove node and its virtual_copies from the hash ring 
        """
        for i in range(self.virtual_copies):
            key = self.get_hash(f"{node}#{i}")
            del self.ring[key]
            self._sorted_keys.remove(key)
            self.redistribute_objects(node)

    def redistribute_objects(self, node):
        # TODO：think about how to redistribute objects after add or delete the node
        pass

    def get_node(self, key):
        """
        Given a key， a corresponding node in the hash ring is returned.

        If the hash ring is empty, `None` is returned.
        """
        return self.find_responsible_node(key)[0]

    def find_responsible_node(self, key):
        """
        Given a key， a corresponding node in the hash ring is returned
        along with its position in the ring.

        If the hash ring is empty, (`None`, `None`) is returned.
        """
        if not self.ring:
            return None, None

        key = self.get_hash(key)
        nodes = self._sorted_keys
        for i in range(len(nodes)):
            node = nodes[i]
            if key < node:
                return self.ring[node], i

        return self.ring[nodes[0]], 0

    def get_hash(self, key):
        """
        Given a key, it returns a long value, which represents
        a place on the hash ring
        """
        m = hashlib.md5()
        m.update(key.encode('utf-8'))
        return m.hexdigest()
