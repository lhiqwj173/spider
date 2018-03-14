# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
from pymongo import MongoClient
from scrapy.conf import settings


class OnejavPipeline(object):
    def open_spider(self, spider):
        self.f = open("2_27.json", "w")

    def process_item(self, item, spider):
        print(item)
        self.f.write(str(item))
        self.f.write("\n")

    def close_spider(self, spider):
        self.f.close()


class MongoPipeline(object):
    def __init__(self):
        # 读取配置参数
        host = settings['MONGO_HOST']
        port = settings['MONGO_PORT']
        dbname = settings['MONGO_DBNAME']
        colname = settings['MONGO_COLNAME']

        # 链接mongodb数据库
        self.handle = MongoClient(host, port)

        # 选择数据库
        self.db = self.handle[dbname]

        # 选择集合
        self.col = self.db[colname]
        self.start = time.time()

    def process_item(self, item, spider):
        print(item)
        # 将item实例转化成字典
        data = dict(item)
        # 写入数据库
        self.col.insert(data)

        # 返回item
        return item

    def close_spider(self, spider):
        # 关闭数据库链接
        self.handle.close()
        end = time.time()
        print("爬虫耗时：{} 秒".format(end - self.start))
