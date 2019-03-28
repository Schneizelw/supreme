# -*- coding:utf-8 -*-
import json
import redis
import random 

MAX_IP_SCORE = 50
HIGHLY_PROXY_SCORE = 100
MIN_IP_SCORE = 0
INIT_IP_SCORE = 10

class RiverEndError(Exception):
    def __str__(self):
        return repr("proxy is not left")

class RedisClient():
    
    def __init__(self):
        """
            open config file to connect redis
        """
        fd = open("conf/redis_config.json", "r")
        tmp = fd.read()
        data = json.loads(tmp)
        self.database = redis.StrictRedis(
            host=data["host"], 
            port=data["port"], 
            password=None,
            decode_responses=True
        )
        self.key = data["key"]

    def exists(self, proxy):
        """
            determine whether a proxy is present
        """
        return not self.database.zscore(self.key, proxy) == None

    def add(self, proxy):
        """
            add a new proxy
        """
        if not self.exists(proxy):
            mapping = {
                proxy : INIT_IP_SCORE
            }
            return self.database.zadd(self.key, mapping)
    
    def add_proxies(self, proxies):
        """
            add proxies
        """
        for proxy in proxies:
            self.add(proxy)

    def add_highly(self, proxy):
        """
            add a new highly proxy
        """
        if not self.exists(proxy):
            mapping = {
                proxy : HIGHLY_PROXY_SCORE - 1
            }
            return self.database.zadd(self.key, mapping)

    def add_highly_proxies(self, proxies):
        """
            add highly proxies
        """
        for proxy in proxies:
            self.add_highly(proxy)

    def count(self):
        """
            return number of the proxies
        """
        return self.database.zcard(self.key)
    
    def all(self):
        """
            get all proxies
        """
        return self.database.zrangebyscore(self.key, MIN_IP_SCORE, MAX_IP_SCORE)

    def max(self, proxy):
        """
            set proxy's score to max
        """
        #print("proxy can be use: %s" % proxy)
        mapping = { proxy : MAX_IP_SCORE }
        return self.database.zadd(self.key, mapping)

    def set_score(self, proxy, score):
        """
            set proxy's score to max
        """
        #print("proxy can be use: %s" % proxy)
        mapping = { proxy : score }
        return self.database.zadd(self.key, mapping)

    def get_proxy(self):
        """ 
            get a proxy can be use by random
        """
        result = self.database.zrangebyscore(self.key, MAX_IP_SCORE, MAX_IP_SCORE)
        if len(result):
            return random.choice(result)
        else:
            #山穷水尽
            raise RiverEndError
    
    def get_highly_proxy(self):
        """ 
            get highly proxy
        """
        result = self.database.zrangebyscore(self.key, HIGHLY_PROXY_SCORE, HIGHLY_PROXY_SCORE)
        if len(result):
            return random.choice(result)
        else:
            return self.get_proxy()

    def decrease(self, proxy):
        """
            reduce one point
        """
        score =  self.database.zscore(self.key, proxy)
        if score and score > MIN_IP_SCORE:
            return self.database.zincrby(self.key, -1, proxy)
        else:
            print("delete %s" % proxy)
            return self.database.zrem(self.key, proxy)
    
    def get_score(self, proxy):
        """
            return proxy score
        """
        score =  self.database.zscore(self.key, proxy)
        return score 
