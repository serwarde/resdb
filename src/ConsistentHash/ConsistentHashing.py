import hashlib
class ConsistentHashing():

    def __init__(self, nodes=None, virtual_copies=1):
        """
        initialize
        """
        self.virtual_copies = virtual_copies
        self.ring = dict()
        self._sorted_hashcode = []

        if nodes:
            for node in nodes:
                self.init_ring(node)

    def init_ring(self, node):
        """
        Initialize the hash ring
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
        self.redistribute_objects_for_add(node)

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
        """Find the corresponding key of the object, whose hashvalue is in the related range,
           put it into the new node.
        """
        # TODO：think about how to redistribute objects when considering virtual nodes
        hashcode = self.get_hash(node._host_name + '#' + str(0))
        position = self._sorted_hashcode.index(hashcode)

        if position == 0:
            prev_neighbor_hashcode = self._sorted_hashcode[-1]
            next_neighbor_hashcode = self._sorted_hashcode[position + 1]
            next_neighbor_node = self.ring[next_neighbor_hashcode]

        elif position == len(self._sorted_hashcode) - 1:
            prev_neighbor_hashcode = self._sorted_hashcode[position - 1]
            next_neighbor_hashcode = self._sorted_hashcode[0]
            next_neighbor_node = self.ring[next_neighbor_hashcode]
        else:
            prev_neighbor_hashcode = self._sorted_hashcode[position - 1]
            next_neighbor_hashcode = self._sorted_hashcode[position + 1]
            next_neighbor_node = self.ring[next_neighbor_hashcode]

        #         all_object = next_neighbor_node._objects_dict
        for k, v in next_neighbor_node._objects_dict.items():
            if k > prev_neighbor_hashcode and k < hashcode:
                node.add_object(k, v)
                next_neighbor_node.remove_object(k, v)

    def redistribute_objects_for_remove(self, node):
        """Find all objects stored on the current node,
           put them into the next node.
        """
        # TODO：think about how to redistribute objects when considering virtual nodes
        hashcode = self.get_hash(node._host_name + '#' + str(0))
        position = self._sorted_hashcode.index(hashcode)
        # prev_neighbor_hashcode = self._sorted_hashcode[position - 1]
        print(node._host_name, position)
        if position == len(self._sorted_hashcode) - 1:
            next_neighbor_hashcode = self._sorted_hashcode[0]
            next_neighbor_node = self.ring[next_neighbor_hashcode]
        else:
            next_neighbor_hashcode = self._sorted_hashcode[position + 1]
            next_neighbor_node = self.ring[next_neighbor_hashcode]

        #         all_object = node._objects_dict
        for k, v in node._objects_dict.items():
            next_neighbor_node.add_object(k, v)

        # all_object = node._objects_dict
        # # remove_node(node)
        for i in range(self.virtual_copies):
            hashcode = self.get_hash(f"{node._host_name}#{i}")
            del self.ring[hashcode]
            # self.redistribute_objects_for_remove(node)
            self._sorted_hashcode.remove(hashcode)

    #         for k,v in node._objects_dict.items():
    #             responsible_node, _ = find_responsible_node(k)
    #             responsible_node.add_object(k,v)

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

        hashcode = self.get_hash(key)
        nodes = self._sorted_hashcode
        for i in range(len(nodes)):
            node = nodes[i]
            if node > hashcode:
                return self.ring[node], i
                break

        return self.ring[nodes[0]], 0

    def get_hash(self, key):
        """
        Given a key, it returns a long value, which represents
        a place on the hash ring
        """
        m = hashlib.md5()
        m.update(key.encode('utf-8'))
        return m.hexdigest()
