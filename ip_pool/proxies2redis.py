import time
from redis_client import RedisClient
from get_proxies import Crawler

POOL_THRESHOLD = 10000

class Save():
    
    def __init__(self):
        #连接redis
        self.redis = RedisClient()
        #初始化爬虫模块
        self.crawler = Crawler()

    def proxies2redis(self):
        #检查redis中目前代理数量 小于10000则继续爬取代理
        if self.redis.count() < POOL_THRESHOLD:
            start = time.time() 
            # 调用每一个爬虫函数爬取代理
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
       
