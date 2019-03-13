# -*- coding: utf-8 -*-
import scrapy
import time
import requests
from scrapy import Request, Spider
from qfang.items import NewHouseItem

class QfangcomSpider(scrapy.Spider):
    name = 'qfangcom'
    allowed_domains = ['qfang.com']
    #记录当前遍历到的city
    city = ""
    cities = ["shenzhen"]
    base_url = "https://{city}.qfang.com"
    qfang_url = "https://{city}.qfang.com/newhouse/list/u1-u2-{page}"

    def start_requests(self):
        begin = "n1"
        for city in self.cities:
            self.city = city
            yield Request(self.qfang_url.format(city=city,page=begin), 
                callback = self.parse_start, dont_filter=True)

    def parse_single(self, response):
        item = NewHouseItem()
        lis = response.css("#scrollto-4 .basic-info-newhs.clearfix ul li")
        order = [
            "_id", "plot_ratio",
            "region", "landscaping_ratio",
            "price", "households",
            "decoration", "parking_num", 
            "property_use", "area", 
            "property_limit", "property_company", 
            "open_time", "property_charges", 
            "delivery_time", "license", 
            "location", "developer"
        ]
        for index, li in enumerate(lis):
            text = li.css("p.correspondence::text").extract_first()
            item[order[index]] = text
        item["url"] = response.meta["url"]
        item["city"] = self.city
        yield item
 
    def parse_main(self, response):
        #print(response.text)
        lis = response.css("#newhouse-list li")
        jump_advertisement = 0
        for li in lis:
            jump_advertisement += 1
            if jump_advertisement == 4:
                continue
            print("line: ", jump_advertisement)
            path = li.css(".new-house-detail .house-title a::attr('href')").extract_first()
            url = self.base_url.format(city=self.city)
            url += path
            yield Request(url=url, meta={"url": url}, callback=self.parse_single, dont_filter=True)

    def parse_start(self, response):
        pages = response.css(".turnpage_num.fr a")
        text = pages[-1].css("a::text").extract_first()
        #获取到最后一页的页码
        last_page = int(text.strip())
        #遍历每一主页
        for page in range(last_page+1):
            page_str = "n" + str(page)
            url = self.qfang_url.format(city=self.city, page=page_str)
            yield Request(url=url, callback=self.parse_main, dont_filter=True)
