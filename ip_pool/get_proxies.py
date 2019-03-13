# -*- coding:utf-8 -*-
import json
import time
import requests
from pyquery import PyQuery as pq
from requests.exceptions import ConnectionError

class Metaclass(type):

    def __new__(cls, name, bases, attrs):
        count = 0
        attrs["__Funcs__"] = []
        for name, _ in attrs.items():
            if "crawl_" in name:
                attrs["__Funcs__"].append(name)
                count += 1
        attrs["__FuncCount__"] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(metaclass=Metaclass):
   
    def __init__(self):
        fd = open("conf/proxy_url.json", "r")
        tmp = fd.read()
        self.urls = json.loads(tmp)

    def get_html(self, url):
        """
            reqeust url and get html
        """
        headers = {
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
        }
        try:
            resp = requests.get(url, headers=headers)
            if resp.status_code == 200:
                return resp.text
        except ConnectionError:
            print("get html failed!! url : %s" % url)
            return None

    def get_proxies(self, func):
        """
            exec all crawl func to get proxies and get a proxy list
        """
        proxies = []
        for proxy in eval("self.{}()".format(func)):
            print("succ get proxy", proxy)
            proxies.append(proxy)
        return proxies

    
    def crawl_66ip(self):
        """
            get 66ip proxy
        """
        upper_limit = 5
        url_66ip = self.urls["66ip"]
        url_list = [url_66ip.format(page) for page in range(1, upper_limit + 1)]
        for url in url_list:
            print("[66ip]:\tcrawl url:%s" % url)
            time.sleep(0.5)
            html = self.get_html(url)
            if html:
                doc = pq(html)
                trs = doc(".containerbox table tr:gt(0)").items()
                for tr in trs:
                    ip = tr.find("td:nth-child(1)").text()
                    port = tr.find("td:nth-child(2)").text()
                    yield ip + ':' + port

    def crawl_kuaiproxy(self):
        """
            get kuaiproxy 
        """
        upper_limit = 5
        url_kuai = self.urls["kuaiproxy"]
        url_list = [url_kuai.format(page) for page in range(1, upper_limit + 1)]
        for url in url_list:
            print("[kuaiproxy]:\tcrawl url:%s" % url)
            time.sleep(1)
            html = self.get_html(url)
            if html:
                doc = pq(html)
                trs = doc("#list table.table-bordered tr:gt(0)").items()
                for tr in trs:
                    ip = tr.find("td:nth-child(1)").text()
                    port = tr.find("td:nth-child(2)").text()
                    yield ip + ":" + port
    
    def crawl_xiciproxy(self):
        """
            get xiciproxy 
        """
        upper_limit = 5
        url_xici = self.urls["xiciproxy"]
        url_list = [url_xici.format(page) for page in range(1, upper_limit + 1)]
        for url in url_list:
            print("[xiciproxy]:\tcrawl url:%s" % url)
            time.sleep(0.5)
            html = self.get_html(url)
            if html:
                doc = pq(html)
                trs = doc("#ip_list tr:gt(1)").items()
                for tr in trs:
                    ip = tr.find("td:nth-child(2)").text()
                    port = tr.find("td:nth-child(3)").text()
                    yield ip + ":" + port



    def crawl_89proxy(self):
        """
            get 89proxy 
        """
        upper_limit = 5
        url_89 = self.urls["89proxy"]
        url_list = [url_89.format(page) for page in range(1, upper_limit + 1)]
        for url in url_list:
            print("[89proxy]:\tcrawl url:%s" % url)
            time.sleep(0.5)
            html = self.get_html(url)
            if html:
                doc = pq(html)
                trs = doc(".layui-form .layui-table tr:gt(0)").items()
                for tr in trs:
                    ip = tr.find("td:nth-child(1)").text().strip()
                    port = tr.find("td:nth-child(2)").text().strip()
                    yield ip + ":" + port
