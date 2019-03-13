# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import json
import random
import requests
from scrapy import signals

class CookiesMiddleware():
    
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(cookies_url = settings["COOKIE_URL"])  

    def __init__(self, cookies_url):
        #self.logger = logging.get_Logger(__name__)
        self.cookies_url = cookies_url

    def get_cookie(self):
        try:
            res = requests.get(self.cookies_url)
            if res.status_code == 200:
                cookie = json.loads(res.text)
                return cookie
        except Exception as e:
            print("get cookie err %s" % str(e))
            return False
    
    def process_request(self, request, spider):
        """
            请求url的时候会先调用该函数
        """
        cookie = self.get_cookie()
        if cookie:
            #设置cookie
            request.cookies = cookie
            print("succ set cookie")

class ProxyMiddleware():
    
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(proxy_url = settings["PROXY_URL"])

    def __init__(self, proxy_url):
        self.proxy_url = proxy_url

    def get_proxy(self):
        try:
            print(self.proxy_url)
            res = requests.get(self.proxy_url)
            if res.status_code == 200:
                proxy = res.text
                return proxy
        except Exception as e:
            print("get proxy err: %s" % str(e))
            return False

    def process_request(self, request, spider):
        if request.meta.get("retry_times"):
            proxy = self.get_proxy()
            if proxy:
                uri = "https://{proxy}".format(proxy=proxy)
                request.meta["proxy"] = uri
                print("succ set proxy")


class UserAgentMiddleware():

    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36"
        ]

    def process_request(self, request, spider):
        request.headers["User-Agent"] = random.choice(self.user_agents)
