# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from lianjia.items import NewHouseItem, BasicInfoItem
from lianjia.items import PlanInfoItem, AroundInfoItem

class LianjiaPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, NewHouseItem):
            item["basic_info"] = {}
            item["plan_info"] = {}
            item["around_info"] = {}
        elif isinstance(item, BasicInfoItem):
            item["price"] = item["price"].replace("均价", "").strip()
            item["tag"] = item["tag"].strip().split(" ")
        elif isinstance(item, PlanInfoItem):
            for k, v in item.items():
                if v is not None and isinstance(v, str):
                    item[k] = v.strip()
        elif isinstance(item, AroundInfoItem):
            for k, v in item.items():
                if v is not None and isinstance(v, str):
                    item[k] = v.strip().replace("\n", "").replace(" ", "").replace("；","")
        return item
        
class MongoPipeline(object):
    
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings.get("MONGO_URI"),
            mongo_db = crawler.settings.get("MONGO_DB"),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        if isinstance(item, NewHouseItem):
            self.db[item.collection].update(
                {"_id" : item["_id"]},
                {"$set" : dict(item)},
                True
            )  
            return item
        if isinstance(item, (BasicInfoItem, PlanInfoItem, AroundInfoItem)):
            page_id = item["_id"]
            item.pop("_id")
            self.db[item.collection].update(
                {"_id" : page_id},
                {"$set" : {item.info : dict(item)}},
                True
            )
            return item
