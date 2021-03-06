import time
from cookie_server import app
from check_cookies import WebCheck
from get_cookies import Generator
from multiprocessing import Process

CHECK_CYCLE = 60
GENERATE_CYCLE = 60
API_HOST = "0.0.0.0"
API_PORT = 8051
GENERATOR_OPEN = True
CHECK_OPEN = True
SERVER_OPEN = True

cookies_list = [
#    "qfang",
    "lianjia"
]

class CookiePool():

    @staticmethod
    def check_cookies():
        while True:
            for site in cookies_list:
                check = WebCheck(site)
            try:
                check.check()
                time.sleep(CHECK_CYCLE)
            except Exception as e:
                print("check cookies err : %s" % str(e))

    @staticmethod
    def generate_cookies():
        while True:
            for site in cookies_list:
                generator = Generator(site)
                try:
                    generator.save_cookies()
                    generator.close()
                    time.sleep(GENERATE_CYCLE)
                except Exception as e:
                    generator.close()
                    print("generate cookies err %s" % str(e))

    @staticmethod
    def cookies_server():
        app.run(host=API_HOST, port=API_PORT)

    def start(self):
        if SERVER_OPEN:
            api_process = Process(target=CookiePool.cookies_server)
            api_process.start()

        if GENERATOR_OPEN:
            generator_process = Process(target=CookiePool.generate_cookies)
            generator_process.start()

        if CHECK_OPEN:
            check_process = Process(target=CookiePool.check_cookies)
            check_process.start()

if __name__ == "__main__":    
    obj = CookiePool()
    obj.start()
