# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import json
import time
import random
import requests
from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
            if request.url[-7:] != "execute":
                #设置cookie
                request.cookies = cookie
                print("succ set cookie")
            else:
                request.meta["splash"]["args"]["cookies"] = cookie

class ProxyMiddleware():
    
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(proxy_url = settings["PROXY_URL"])

    def __init__(self, proxy_url):
        self.proxy_url = proxy_url

    def get_proxy(self):
        try:
            res = requests.get(self.proxy_url)
            if res.status_code == 200:
                proxy = res.text
                return proxy
        except Exception as e:
            print("get proxy err: %s" % str(e))
            return False

    def process_request(self, request, spider):
        proxy = self.get_proxy()
        if proxy:
            if request.url[-7:] != "execute":
                uri = "https://{proxy}".format(proxy=proxy)
                print(uri)
                request.meta["proxy"] = uri
                print("succ set proxy")
            else:
                res = proxy.split(":")
                request.meta["splash"]["args"]["host"] = res[0]
                request.meta["splash"]["args"]["port"] = res[1]


class UserAgentMiddleware():

    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
            "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
        ]

    def process_request(self, request, spider):
        if request.url[-7:] != "execute":
            request.headers["User-Agent"] = random.choice(self.user_agents)
        else:
            request.meta["splash"]["user_agent"] = random.choice(self.user_agents)
            

class SeleniumMiddleware():
    
    def __init__(self, timeout):
        self.timeout = timeout
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1980,1980')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.wait = WebDriverWait(self.browser, self.timeout)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            timeout=crawler.settings.get('SELENIUM_TIMEOUT')
        )

    def __del__(self):
        self.browser.close()

    def process_request(self, request, spider):
        """
            对详情页插入selenium渲染，等待js代码渲染获取得到学校，医院等数据
        """
        url = request.url
        if url[-9:] != "xiangqing":
            return None
        try:
            self.browser.get(url)
            self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#around_txt div span.ret span")
            ))
            return HtmlResponse(url=url, body=self.browser.page_source, 
                request=request, encoding="utf-8", status=200)
        except TimeoutException:
            print("drop this page %s" % url)
            return None
       
