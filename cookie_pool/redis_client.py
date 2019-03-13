import json
import redis
import random

class RedisClient():

    def __init__(self, type, website):
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
        self.name = "{}:{}".format(type, website)

    def set(self, user, value):
        """
            set pair(user:password or user:cookie)
        """
        return self.database.hset(self.name, user, value)

    def get(self, user):
        """
            get value by user
        """
        return self.database.hget(self.name, user)
        
    def delete(self, user):
        """
            delete value by user
        """
        print("delete",user)
        return self.database.hdel(self.name, user)

    def count(self):
        """
            return cookie count
        """
        return self.database.hlen(self.name)

    def get_cookie(self):
        """
            get cookie by random
        """
        return random.choice(self.database.hvals(self.name))

    def all_users(self):
        """
            get all username
        """
        return self.database.hkeys(self.name)

    def all_pairs(self):
        """
            get all pair(user:password or user:cookie)
        """
        return self.database.hgetall(self.name)
