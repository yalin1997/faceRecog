
from multiprocessing.managers import BaseManager
from multiprocessing import RLock , Queue


MANAGER_PORT = 6000
MANAGER_DOMAIN = '0.0.0.0'
MANAGER_AUTH_KEY = b"nknuwe310a"
class QueueManager(BaseManager):
    pass

class QueueItem():
    def __init__(self, ):
        self.items = Queue()

    def set(self, value):
        self.items.put(value)

    def get(self):
        if self.items.not_empty:
            value = self.items.get()
        else:
            value = None
        return value

class isRuning():
    def __init__(self , ):
        self.runing = False
    def set(self):
        if this.runing :
            self.runing = False
        else:
            self.runing = True

    def get(self):
        return self.runing
        

d = QueueItem()
lock = RLock()
runing = isRuning()

QueueManager.register('queue', callable=lambda: d)
QueueManager.register('open_qq_login_lock', callable=lambda: lock)
QueueManager.register('isRuning' , callable=lambda: runing)
class ManagerServer():
    
    # multiprocess Manager 服務Class
    
    def __init__(self, domain, port, auth_key):
        self.domain = domain
        self.port = port
        self.auth_key = auth_key

    def start_manager_server(self):
        self.queue_manager = QueueManager(address=('', self.port), authkey=self.auth_key)
        # self.dict = self.queue_manager.dict()
        self.server = self.queue_manager.get_server()

    def run(self):
        self.start_manager_server()
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()
        self.is_stop = 1

class ManagerClient():
# Manager server client
    def __init__(self, domain, port, auth_key):
        self.domain = domain
        self.port = port
        self.auth_key = auth_key
        # self.get_share_dict()
        self.info_manager = QueueManager(address=(self.domain, self.port), authkey=self.auth_key)
        self.info_manager.connect()

    def getQueue(self):
        # self.dict = m.dict()
        self.queue = self.info_manager.queue()
        return self.queue

    def get_open_qq_login_lock(self):
        self.open_qq_login_lock = self.info_manager.open_qq_login_lock()
        return self.open_qq_login_lock

    def getIsRuning(self):
        return self.info_manager.isRuning()

if __name__ == '__main__':
    manager_server = ManagerServer(MANAGER_DOMAIN, MANAGER_PORT, MANAGER_AUTH_KEY)
    manager_server.run()

