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
       
