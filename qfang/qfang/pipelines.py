# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class QfangPipeline(object):

    def process_item(self, item, spider):
        for key, value in item.items():
            if value != None:
                item[key] = value.strip()
                item[key] = value.replace("\t","").replace("\n","")
                item[key] = value.replace(" ","").replace("\r","")
            if key == "property_charges":
                value[-2] == "/"
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
        self.db[item.__class__.__name__].update(
            {"_id": item["_id"]},
            {"$setOnInsert": dict(item)},
            upsert=True
        )
        #self.db[self.collection].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()
