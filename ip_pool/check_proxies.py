# -*- coding:utf-8 -*-
import time
import random
import asyncio 
import aiohttp
from redis_client import RedisClient
from concurrent.futures._base import TimeoutError
from aiohttp.client_exceptions import ServerDisconnectedError
from aiohttp.client_exceptions import ClientResponseError
VALID_STATUS_CODES = [200]
CHECK_URL = [
    "http://sz.lianjia.com/", 
]
CHECK_SIZE = 80

class Check():
    
    def __init__(self):
        self.redis = RedisClient()

    async def check_single(self, proxy):
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode("utf-8")
                real_proxy = "http://" + proxy               
                check_url = CHECK_URL[random.randint(0, len(CHECK_URL)-1)]
                print("checking: ",real_proxy, check_url)
                async with session.get(check_url, proxy=real_proxy, timeout=10) as response:
                    score = self.redis.get_score(proxy)
                    if response.status in VALID_STATUS_CODES:
                        if score != 100:
                            #设置到50分 
                            self.redis.max(proxy)
                            print("%s can be use 50 score" % proxy)
                    else:
                        print("1:Not valid code:%s decrease" % proxy)
                        if socore == 51:
                           self.redis.delproxy(proxy)
                        else:
                            self.redis.decrease(proxy)
            except (TimeoutError, OSError, ServerDisconnectedError,ClientResponseError) as e:
                print("2:Catch Error error:%s %s decrese" % (str(e),proxy))
                self.redis.decrease(proxy)

    def check(self):
        try:
            proxies = self.redis.all()
            loop = asyncio.get_event_loop()
            for index in range(0, len(proxies), CHECK_SIZE):
                check_proxies = proxies[index:index + CHECK_SIZE]
                tasks = [self.check_single(proxy) for proxy in check_proxies]
                #把多个写成放进一个事件循环
                loop.run_until_complete(asyncio.wait(tasks))
        except Exception as e:
            print("check err: %s" % str(e))


if __name__ == "__main__":
    obj = Check()
    obj.check()
