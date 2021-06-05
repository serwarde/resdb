import random

class LoadBalancer():
    
    _router_list = [1,23]
    
    def request(self,type,key,value=None):    
        '''
        gets a request from the user and calculates the responsible node
        and the forwards the request to this node
        
        type = can be (get, add, remove or update)
        key = the key for the item that should be stored
        value = only necessary for add and update
        '''
         
        router = self.get_random_router()
        node = router.find_responsible_node(key)
        node.get_request(type, key, value)
    
    def get_random_router(self):
        """
        Return a random_router
        """
        # TODO: Improve the strategy of choosing a router
        return random.choice(self.get_router_list())
    
    def get_router_list(self):
        """
        Returns the router_list
        """
        return self._router_list