# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from scrapy.conf import settings
from datetime import datetime


class MeituluPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    def __init__(self):
        # 读取配置参数
        host = settings['MONGO_HOST']
        port = settings['MONGO_PORT']
        dbname = settings['MONGO_DBNAME']
        colname = settings['MONGO_COLNAME']

        now_str = datetime.now().strftime("%m_%d_%H_%M")
        colname += "_" + now_str
        # 链接mongodb数据库
        self.handle = MongoClient(host, port)

        # 选择数据库
        self.db = self.handle[dbname]

        # 选择集合
        self.col = self.db[colname]

    def process_item(self, item, spider):
        # print(item)
        # 1. 使用model_id做主键
        data = dict(item)  # 将item实例转化成字典
        data["_id"] = data.pop("model_id")
        # 2. 查询库中数据是否已存在，不存在才存
        res = self.col.find_one({"_id": data["_id"]})
        if not res:
            self.col.insert(data)  # 写入数据库

        # 返回item
        return item

    def close_spider(self, spider):
        # 关闭数据库链接
        self.handle.close()
