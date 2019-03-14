# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.org/en/latest/topics/items.html

import scrapy
from scrapy import Item,Field

class NewHouseItem(Item):
    # define the fields for your item here like:
    collection = "newHouse"
    # id
    _id = Field()
    # 房产名字
    name = Field()
    # 容积率
    plot_ratio = Field()
    # 所属区域
    region = Field()
    # 绿化率
    landscaping_ratio = Field()
    # 参考均价
    price = Field()
    # 总户数
    households = Field()
    # 装修情况
    decoration = Field()
    # 车位数量
    parking_num = Field()
    # 物业用途
    property_use = Field()
    # 占地面积
    area = Field()
    # 产权年限
    property_limit = Field()
    # 物业公司
    property_company = Field()
    # 开盘时间
    open_time = Field()
    # 物业费用
    property_charges = Field()
    # 交房时间
    delivery_time = Field()
    # 预售许可证
    license = Field()
    # 楼盘地址
    location = Field()
    # 开放商
    developer = Field()
    # 网站url
    url = Field()
    # 城市
    city = Field()
    # 几室几厅 面积 一套的价格
    house_type = Field()

class HouseTypeItem(Item):
    collection = "newHouse"
    _id = Field()
    house_type = Field()
