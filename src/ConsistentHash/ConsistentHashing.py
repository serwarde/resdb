import hashlib


class ConsistentHashing():

    def __init__(self, nodes=None, virtual_copies=10):
        """
        initialize
        """
        self.virtual_copies = virtual_copies
        self.ring = dict()
        self._sorted_hashcode = []
        self.preference_list_num = 3

        if nodes:
            for node in nodes:
                self.init_ring(node)

    def init_ring(self, node):
        """
        initialize the hash ring
        """
        for i in range(self.virtual_copies):
            virtual_node = f"{node._host_name}#{i}"
            hashcode = self.get_hash(virtual_node)
            self.ring[hashcode] = node
            self._sorted_hashcode.append(hashcode)
        self._sorted_hashcode.sort()

    def add_node(self, node):
        """
        Add a new node and its virtual nodes into the hash ring
        """
        for i in range(self.virtual_copies):
            virtual_node = f"{node._host_name}#{i}"
            hashcode = self.get_hash(virtual_node)
            self.ring[hashcode] = node
            self._sorted_hashcode.append(hashcode)

        self._sorted_hashcode.sort()
        # self.redistribute_objects_for_add(node)

    def remove_node(self, node):
        """
        Remove node and its virtual_copies from the hash ring
        """
        for i in range(self.virtual_copies):
            hashcode = self.get_hash(f"{node._host_name}#{i}")
            del self.ring[hashcode]
            # self.redistribute_objects_for_remove(node)
            self._sorted_hashcode.remove(hashcode)

    def redistribute_objects_for_add(self, node):
        """
        Find a corresponding key of the object, whose hashvalue is in the related range,
        put it into the new node.
        """
       
        hashcode = self.get_hash(node._host_name + '#' + str(0))
        position = self._sorted_hashcode.index(hashcode)

        if position == 0: # The first position of hashring
            prev_neighbor_hashcode = self._sorted_hashcode[-1]
            next_neighbor_hashcode = self._sorted_hashcode[position + 1]
            next_neighbor_node = self.ring[next_neighbor_hashcode]

        elif position == len(self._sorted_hashcode) - 1: # The last position of hashring
            prev_neighbor_hashcode = self._sorted_hashcode[position - 1]
            next_neighbor_hashcode = self._sorted_hashcode[0]
            next_neighbor_node = self.ring[next_neighbor_hashcode]
        else: # Other
            prev_neighbor_hashcode = self._sorted_hashcode[position - 1]
            next_neighbor_hashcode = self._sorted_hashcode[position + 1]
            next_neighbor_node = self.ring[next_neighbor_hashcode]

        #         all_object = next_neighbor_node._objects_dict
        # Move the object that in the specific region into the new node
        for k, v in next_neighbor_node._objects_dict.items():
            if k > prev_neighbor_hashcode and k < hashcode:
                node.add_object(k, v)
                next_neighbor_node.remove_object(k, v)

    def redistribute_objects_for_remove(self, node):
        """
        Find all objects stored on the current node,
        put them into the next node.
        """
        hashcode = self.get_hash(node._host_name + '#' + str(0))
        position = self._sorted_hashcode.index(hashcode)

        if position == len(self._sorted_hashcode) - 1:
            next_neighbor_hashcode = self._sorted_hashcode[0]
            next_neighbor_node = self.ring[next_neighbor_hashcode]
        else:
            next_neighbor_hashcode = self._sorted_hashcode[position + 1]
            next_neighbor_node = self.ring[next_neighbor_hashcode]

        #         all_object = node._objects_dict
        for k, v in node._objects_dict.items():
            next_neighbor_node.add_object(k, v)




    def find_preference_list(self, key):
        """
        Given a key， return the corresponding preference list.
        preference list = N neighbor nodes after the responsible node.

        If the hash ring is empty, (`None`, `None`) is returned.
        """
        if not self.ring:
            return None, None
        preferrence_list = []

        hashcode = self.get_hash(key)
        nodes = self._sorted_hashcode
        for node_hash in self._sorted_hashcode:
            if node_hash > hashcode:
                preferrence_list.append(node_hash)

        preferrence_list = preferrence_list[:self.preference_list_num]
        preferrence_list = [self.ring[node_hash] for node_hash in preferrence_list]
        return preferrence_list, 0


    def get_hash(self, key):
        """
        Given a key, it returns a long value, which represents
        a place on the hash ring
        """
        m = hashlib.md5()
        m.update(key.encode('utf-8'))
        return m.hexdigest()
