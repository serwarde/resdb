class LoadBalancer():
    
    _router_list = [1,23]
    
    def request(self,type,key,value=None):     
        router = self.get_random_router()
        node = router.find_responsible_node(key)
        node.get_request(type, key, value)
    
    def get_random_router(self):
        # todo
        return -1
    
    def get_router_list(self):
        return self._router_list