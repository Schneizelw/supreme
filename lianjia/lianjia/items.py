# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field

class NewHouseItem(Item):
    # define the fields for your item here like:
    collection = "newHouse"
    _id = Field()         # 楼盘id
    url = Field()         # url
    city = Field()        # 城市
    basic_info = Field()  # 基本信息
    plan_info = Field()   # 规划信息
    around_info = Field() # 配套信息

class BasicInfoItem(Item):
    collection = "newHouse"
    info = "basic_info"
    _id = Field()
    name = Field()          # 楼盘名字
    property_type = Field() # 物业类型
    price = Field()         # 参考价格
    tag = Field()           # 房产标签
    region = Field()        # 所属区域
    location = Field()      # 楼盘位置
    sales_office = Field()  # 售楼处
    developer = Field()     # 开发商

class PlanInfoItem(Item):
    collection = "newHouse"
    info = "plan_info"
    _id = Field()
    building_type = Field()    # 建筑类型
    green_ratio = Field()      # 绿化率
    area = Field()             # 占地面积
    build_area = Field()       # 建筑面积
    households = Field()       # 户数 
    property_limit = Field()   # 产权年限
    house_type = Field()       # 户型

class AroundInfoItem(Item):
    collection = "newHouse"
    info = "around_info"
    _id = Field()
    property_company = Field() # 物业公司
    property_price = Field()   # 物业费
    parking_num = Field()      # 停车位
    subway = Field()           # 地铁
    hospital = Field()         # 医院
    school = Field()           # 学校
    market = Field()           # 超市
    park = Field()             # 公园


class RentHouseItem(Item):
    collection = "rentHouse"
    _id = Field()
    url = Field()           # url
    city = Field()          # 城市
    name = Field()          # 名字
    house_type = Field()    # 基本空间
    price = Field()         # 价格
    location = Field()      # 位置
    area = Field()          # 面积
    orientation = Field()   # 朝向
    agency = Field()        # 中介 总是链家(可扩展)
    tags = Field()           # 标签

