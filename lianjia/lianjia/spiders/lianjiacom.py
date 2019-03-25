# -*- coding: utf-8 -*-
import re
import time
import math
import scrapy
import requests
import logging
from scrapy import Request, Spider
from scrapy.selector import Selector
from scrapy_splash import SplashRequest
from lianjia.items import NewHouseItem, BasicInfoItem
from lianjia.items import PlanInfoItem, AroundInfoItem

class LianjiacomSpider(Spider):

    city = ""
    cities = ["sz"]
    name = 'lianjiacom'
    allowed_domains = ['lianjia.com']

    base_url = "https://{city}.lianjia.com"
    lianjia_url = "https://{city}.fang.lianjia.com/loupan/nhs1{page}"

    def start_requests(self):
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
    
    def parse_single(self, response):
        new_house = NewHouseItem()
        plan_info = PlanInfoItem()
        basic_info = BasicInfoItem()
        around_info = AroundInfoItem()
        city = response.data["city"]
        page_id = response.data["_id"]
        new_house["_id"] = page_id
        new_house["url"] = response.data["url"]
        print(response.data["url"])
        yield new_house
        # init basic_info
        html = Selector(text=response.data["html"])
        tmp = html.css(".container .fl.l-txt a")
        basic_info["name"] = tmp[-2].css("a::text").extract_first()
        lis = response.css(".big-left.fl ul.x-box li")
        basic_info["_id"] = page_id
        basic_info["property_type"] = lis[0].css("span.label-val::text").extract_first() 
        basic_info["price"] = lis[1].css("span.label-val span::text").extract_first() 
        basic_info["tag"] = lis[2].css("span.label-val::text").extract_first() 
        basic_info["region"] = lis[3].css("span.label-val a::text").extract_first() 
        basic_info["location"] = lis[4].css("span.label-val::text").extract_first() 
        basic_info["sales_office"] = lis[5].css("span.label-val::text").extract_first() 
        basic_info["developer"] = lis[6].css("span.label-val::text").extract_first() 
        yield basic_info

        # init plan_info
        plan_info["_id"] = page_id
        tmp = html.css(".big-left.fl ul")
        lis = tmp[2].css("li")
        plan_info["building_type"] = lis[0].css("span.label-val::text").extract_first()
        plan_info["green_ratio"] = lis[1].css("span.label-val::text").extract_first()
        plan_info["area"] = lis[2].css("span.label-val::text").extract_first()
        plan_info["build_area"] = lis[4].css("span.label-val::text").extract_first()
        plan_info["households"] = lis[6].css("span.label-val::text").extract_first()
        plan_info["property_limit"] = lis[7].css("span.label-val::text").extract_first()
        plan_info["house_type"] = []
        yield plan_info

        #init around_info
        around_info["_id"] = page_id
        tmp = html.css(".big-left.fl ul")
        lis = tmp[3].css("li")
        around_info["property_company"] = lis[0].css("span.label-val::text").extract_first()
        around_info["property_price"] = lis[2].css("span.label-val::text").extract_first()
        around_info["parking_num"] = lis[6].css("span.label-val::text").extract_first()
        entity = lis[7].css("#around_txt div")
        entity_map = {
            "0" : "subway",
            "1" : "school",
            "2" : "hospital",
            "3" : "market",
            "4" : "park"
        }
        for i in range(5):
            tmp = []
            spans = entity[i].css(".ret span")
            for span in spans:
                text = span.css("span::text").extract_first()
                tmp.append(text)
            around_info[entity_map[str(i)]] = tmp 
        yield around_info        

    def parse_main(self, response):
        
        city = response.meta["city"]
        XIANGQING = "xiangqing"
        lua_script = """
            function main(splash, args)
                local url = args.url
                splash:init_cookies(args.cookies)
                splash:set_user_agent(splash.args.user_agent)
                splash:on_request(function(request)
                    request:set_proxy{
                        host = args.host,
                        port = args.port
                    }
                end)
                splash:go(url)
                splash:wait(args.wait)
                return {
                    html=splash:html(),
                    url=args.url,
                    city=args.city,
                    _id=args._id,
                }
            end
        """
        lis = response.css("ul.resblock-list-wrapper li")
        for li in lis:
            try:
                path = li.css("a.resblock-img-wrapper::attr('href')").extract_first()
                url = self.base_url.format(city=city)
                url = url + path + XIANGQING
                page_id = path[8:-1]
                yield SplashRequest(
                    url, 
                    self.parse_single, 
                    args={
                        "lua_source" : lua_script,
                        "_id" : page_id,
                        "url" : url,
                        "city" : city,
                        'wait' : 2,
                        'host' : '',
                        'port' : '',
                        'cookies' : '',
                        'user_agent' : '',
                    }, 
                    endpoint="execute",
                    dont_filter=False
                )
            except Exception as e:
                print("[ERROR]parse_main err %s" % str(e))

    def parse_start(self, response):
        city = response.meta["city"]
        tmp = response.css("div.page-box::attr('data-total-count')").extract_first()
        tot = float(tmp)
        #获取到最后一页的页码
        last_page = math.ceil(tot/float(10))
        #遍历每一主页
        #for num in range(1, 4):
        for num in range(1, 1 + last_page):
            page = "pg" + str(num)
            url = self.lianjia_url.format(city=city, page=page)
            yield Request(
                url=url, 
                meta={
                    "city" : city
                },
                callback=self.parse_main, 
                dont_filter=False
            )

