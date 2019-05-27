# _*_ coding: utf-8 _*_
from django.db import models
from mongoengine import *


class RentHouse(Document):
    meta = {
        'collection' : 'rentHouse',
    }
    _id = StringField(required=True)
    url = StringField()            # url
    city = StringField()           # 城市
    name = StringField()           # 名字
    house_type = ListField()       # 基本空间
    price = IntField()             # 价格
    location = StringField()       # 位置
    area = StringField()           # 面积
    orientation = StringField()    # 朝向
    agency = StringField()         # 中介 总是链家(可扩展)
    tags = ListField()             # 标签

class NewHouse(Document):
    meta = {
        'collection' : 'newHouse',
    }
    _id = StringField(required=True)
    url = StringField()            # url
    city = StringField()           # 城市
    name = StringField()           # 名字
    basic_info = DictField()       # 基本信息
    plan_info = DictField()        # 规划信息
    around_info = DictField()      # 配套信息
