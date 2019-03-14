# -*- coding: utf-8 -*-
import re
import time
import scrapy
import requests
from scrapy import Request, Spider
from qfang.items import NewHouseItem,HouseTypeItem

class QfangcomSpider(scrapy.Spider):
    name = 'qfangcom'
    allowed_domains = ['qfang.com']
    #记录当前遍历到的city
    city = ""
    cities = ["shenzhen", "shanghai", "suzhou", "qingdao", 
              "nanjing", "zhuhai","zhongshan", "hangzhou",
              "guangzhou","foshan", "dongguan", "nanning"
              "nantong", "taiyuan", "taicang", "jiaxing",
              "jiangmen"]

    base_url = "https://{city}.qfang.com"
    qfang_url = "https://{city}.qfang.com/newhouse/list/u1-u2-{page}"
    housetype_url = "https://{city}.qfang.com/newhousedetail/getLayOutPage/"\
    + "all/{page_id}?pageSize=100&currentPage=1&sourceCity"

    def start_requests(self):
        begin = "n1"
        for city in self.cities:
            self.city = city
            yield Request(self.qfang_url.format(city=city,page=begin), 
                callback = self.parse_start, dont_filter=True)

    def parse_housetype(self, response):
        item = HouseTypeItem()
        tmp = []
        lis = response.css("#newhsDMF ul li")
        for li in lis:
            line = {}
            div = li.css(".fl.newhs-dmf-center div.clearfix")
            spans = div.css(".title.clearfix span")
            price_span = div.css(".newhs-dmf-price.fr span")
            #设置了house_type中的字段
            line["base_info"] = spans[0].css("span::text").extract_first()
            line["area"] = spans[1].css("span::text").extract_first()  
            line["price"] = price_span.css("span::text").extract_first()
            tmp.append(line)
        item["house_type"] = tmp
        item["_id"] = response.meta["id"]
        yield item

    def parse_single(self, response):
        item = NewHouseItem()
        lis = response.css("#scrollto-4 .basic-info-newhs.clearfix ul li")
        order = [
            "name", "plot_ratio",
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
        res = re.search("(?!.*/).*(?=\?)", response.meta["url"])
        page_id = res.group()
        item["_id"] = page_id 
        item["url"] = response.meta["url"]
        item["city"] = self.city
        yield item
        url = self.housetype_url.format(city=self.city, page_id=page_id) 
        yield Request(url=url, meta={"id": page_id }, callback=self.parse_housetype, dont_filter=True)
 
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
        for page in range(1, last_page+1):
            page_str = "n" + str(page)
            url = self.qfang_url.format(city=self.city, page=page_str)
            yield Request(url=url, callback=self.parse_main, dont_filter=True)
