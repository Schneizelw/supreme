import time
from redis_client import RedisClient
from get_proxies import Crawler

POOL_THRESHOLD = 10000

class Save():
    
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    def proxies2redis(self):
        if self.redis.count() < POOL_THRESHOLD:
            start = time.time() 
            for index in range(self.crawler.__FuncCount__):
                func = self.crawler.__Funcs__[index]
                proxies = self.crawler.get_proxies(func)
                if index == self.crawler.__FuncCount__ - 1:
                    self.redis.add_highly_proxies(proxies) 
                else:
                    self.redis.add_proxies(proxies)
            end = time.time()
            diff = end - start
            print("save proxies 2 redis consuming:", diff)
       
