# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from qfang.items import NewHouseItem, HouseTypeItem

class QfangPipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, NewHouseItem):
            for key, value in item.items():
                if value != None:
                    item[key] = value.strip().replace("\t","").replace("\n","")\
                    .replace(" ","").replace("\r","")
                if key == "property_charges":
                    item[key][-2] == "/"
        if isinstance(item, HouseTypeItem):
            for index, data in enumerate(item["house_type"]):
                item["house_type"][index]["price"] = data["price"]
                item["house_type"][index]["base_info"] = data["base_info"].strip()
                item["house_type"][index]["area"] = data["area"].\
                replace("建筑面积", "").replace("平米", "m2")
        return item

class MongoPipeline():

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
        if isinstance(item, HouseTypeItem):
            self.db[item.collection].update(
                {"_id" : item["_id"]},
                {"$set" : {"house_type" : list(item["house_type"])}},
                True
            )
        return item

    def close_spider(self, spider):
        self.client.close()
