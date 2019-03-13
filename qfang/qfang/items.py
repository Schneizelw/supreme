# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class NewHouseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    plot_ratio = scrapy.Field()
    region = scrapy.Field()
    landscaping_ratio = scrapy.Field()
    price = scrapy.Field()
    households = scrapy.Field()
    decoration = scrapy.Field()
    parking_num = scrapy.Field()
    property_use = scrapy.Field()
    area = scrapy.Field()
    property_limit = scrapy.Field()
    property_company = scrapy.Field()
    open_time = scrapy.Field()
    property_charges = scrapy.Field()
    delivery_time = scrapy.Field()
    license = scrapy.Field()
    location = scrapy.Field()
    developer = scrapy.Field()
    url = scrapy.Field()
    city = scrapy.Field()
