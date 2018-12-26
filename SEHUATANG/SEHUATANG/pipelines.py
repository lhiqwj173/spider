# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
from pymongo import MongoClient


class SehuatangPipeline(object):
    def __init__(self):
        # 读取配置参数
        host = settings["MONGO_HOST"]
        port = settings["MONGO_PORT"]
        dbname = settings["MONGO_DBNAME"]
        colname = settings["MONGO_COLNAME"]

        self.handle = MongoClient(host, port)
        self.col = self.handle[dbname][colname]

    def process_item(self, item, spider):
        print(item)
        self.col.insert(dict(item))
        return item

    def close_spider(self, spider):
        self.handle.close()
