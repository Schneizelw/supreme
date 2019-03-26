import time
from pool_server import app
from proxies2redis import Save
from check_proxies import Check
from multiprocessing import Process

SAVE_CYCLE_TIME = 3600
CHECK_CYCLE_TIME = 30

SAVE_OPEN = True
CHECK_OPEN = True
SERVER_OPEN = True

API_HOST = "0.0.0.0"
API_PORT = 8052

class IpPool():
    
    def check_module(self):
        check = Check()
        while True:
            print("check proxies start!")
            check.check()
            time.sleep(CHECK_CYCLE_TIME)

    def save_module(self):
        save = Save()
        while True:
            print("save proxy to redis start!")
            save.proxies2redis()
            time.sleep(SAVE_CYCLE_TIME)
       
    def server_module(self):
        app.run(API_HOST, API_PORT)

    def start(self):
        print("ip pool start")
        if CHECK_OPEN:
            check_process = Process(target=self.check_module)
            check_process.start()

        if SAVE_OPEN:
            save_process = Process(target=self.save_module)
            save_process.start()

        if SERVER_OPEN:
            server_process = Process(target=self.server_module)
            server_process.start()

if __name__ == "__main__":
    ippool = IpPool()
    ippool.start()
