# -*- coding: utf-8 -*-
import time
import math
import scrapy
import requests
import logging
from scrapy import Request, Spider
from scrapy.selector import Selector
from lianjia.items import RentHouseItem


class RenthouseSpider(scrapy.Spider):
    name = 'renthouse'
    cities = [
        #"bj",
        "sz",
        #"sh", "gz",
        #"cq", "cd", "hz", "wh", "su", "xa", "tj", "nj", "zz", "cs", "sy", "qd", "dg"
    ]
    allowed_domains = ['lianjia.com']
    agency = "ab200301001000"
    base_url = "http://{city}.lianjia.com/zufang"
    lianjia_url = "http://{city}.lianjia.com/zufang/ab200301001000{page}/?showMore=1"

    def start_requests(self):
        """
            对每一个city进行请求 分析主页面
        """
        BEGIN = "pg1"
        for city in self.cities:
            print(self.lianjia_url.format(city=city, page=BEGIN))
            yield Request(
                self.lianjia_url.format(city=city, page=BEGIN), 
                meta={
                    "city" : city
                },
                callback = self.parse_start, 
                dont_filter=True
            )

    def parse_start(self, response):
        """
            获取主页的地区和价格分区 然后分类进行爬虫.
            特殊逻辑：因为linajia只是吐出3000条数据一次性，不分类拿不到全部数据.
            很多城市的房源都是大于3000套的
        """
        RP = "rp"
        city = response.meta["city"]
        zone_lis = response.css("#filter ul:nth-child(2) li")
        zones = []
        for index, li in enumerate(zone_lis):
            if index == 0:
                continue
            link = li.css("a::attr('href')").extract_first()
            elem = link.split('/')
            zones.append(elem[2])
        price_lis = response.css("#filter ul:nth-child(6) li")
        section_count = len(price_lis) - 1
        for zone in zones:
            for i in range(1, section_count):
                pass
                #这里有个特殊逻辑对于链家的请求中 pg==pg1,如果下面构造使用pg1,而dont_filter=False
                #会导致一个问题就是pg1这一页会被去重，每一种地区和价格区间的组合的第一页都会被去
                #掉，用pg等于pg1但是生成fingerprint就不会被去重。
                path = '/' + zone + '/' + self.agency + RP + str(i) + "pg/?showMore=1"
                                                                     #^^^^Warning can't change to pg1
                url = self.base_url.format(city=city) + path
                print(url)
                yield Request(
                    url=url, 
                    meta={
                        "city" : city,
                        "url"  : url,
                    },
                    callback=self.parse_main, 
                    dont_filter=False
                )
        #yield Request(
        #    url="https://sz.lianjia.com/zufang/nanshanqu/ab200301001000rp4pg1/?showMore=1", 
        #    meta={
        #        "city" : city,
        #        "url"  : "https://sz.lianjia.com/zufang/nanshanqu/ab200301001000rp4pg1/?showMore=1",
        #    },
        #    callback=self.parse_main, 
        #    dont_filter=True
        #)

    def parse_main(self, response):
        """
            获取该地区和价格区间组合的页面数量，遍历每一页
        """
        #获取该组合的房源数量判断是否需要翻页
        city = response.meta["city"]
        tmp = response.css("#content .content__article .content__title span::text").extract_first()
        tot = int(tmp)
        #获取到最后一页的页码
        last_page = math.ceil(tot/float(30))
        parent_url = response.meta["url"]
        parent_url = parent_url.replace("pg1", "{page}")
        if last_page != 0:    
            #遍历每一页
            for num in range(1, 1 + last_page):
                page = "pg" + str(num)
                url = parent_url.format(page=page)
                print(url)
                yield Request(
                    url=url, 
                    meta={
                        "city" : city,
                        "url"  : url,
                    },
                    callback=self.parse, 
                    dont_filter=False
                )
            #yield Request(
            #    url="https://sz.lianjia.com/zufang/nanshanqu/ab200301001000rp4pg1/?showMore=1", 
            #    meta={
            #        "city" : city,
            #        "url"  : "https://sz.lianjia.com/zufang/nanshanqu/ab200301001000rp4pg1/?showMore=1",
            #    },
            #    callback=self.parse, 
            #    dont_filter=False
            #)
    
    def parse(self, response): 
        """
            爬取数据
        """
        rent_house = RentHouseItem()
        city = response.meta["city"]
        url = response.meta["url"]
        divs = response.css("#content .content__article .content__list div")
        for index, div in enumerate(divs):
            link = div.css("a::attr('href')").extract_first()
            rent_house["_id"] = link
            rent_house["url"] = url 
            rent_house["city"] = city
            ps = div.css(".content__list--item--main p")
            rent_house["name"] = ps[0].css("a::text").extract_first()
            elems = ps[1].css("p::text").extract()
            if len(elems) > 5:
                rent_house["area"] = elems[3]
                rent_house["orientation"] = elems[4]
                rent_house["house_type"] = elems[5]
            text = ps[1].css("a::text").extract()
            location = '-'.join(text)
            tags = ps[-1].css("i::text").extract()
            price = div.css(".content__list--item--main span em::text").extract_first()
            rent_house["tags"] = tags
            rent_house["price"] = price
            rent_house["location"] = location
            yield rent_house
            

