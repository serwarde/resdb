import time

from rpyc import Service
from rpyc.utils.server import ThreadedServer


class TimeService(Service):
    def exposed_get_time(self):
        return time.ctime()
    
    def exposed_add(self, n1, n2):
        return n1+n2


if __name__ == '__main__':
    s = ThreadedServer(TimeService, port=18871)
    s.start()