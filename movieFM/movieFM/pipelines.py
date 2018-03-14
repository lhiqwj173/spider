# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MoviefmPipeline(object):
    def __init__(self):
        self.file = open("movie.csv", "w", encoding="GBK")
        self.file.write("序号,电影名,年份,类型,导演,评分\n")

    def process_item(self, item, spider):
        # content = ",".join(list(item.values())) + "\n"
        content = item["number"] + "," + item["name"] + "," + item["year"] + "," + item["type"] + "," + item[
            "director"] + "," + item["grade"] + "\n"
        self.file.write(content)
        return item

    def close_spider(self, spider):
        self.file.close()
