# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
from scrapy.conf import settings
from pymongo import MongoClient



class Dytt8Pipeline(object):
    def process_item(self, item, spider):
        return item

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