# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MeituluItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    category = scrapy.Field()
    model_name = scrapy.Field()
    labels = scrapy.Field()
    img_nums = scrapy.Field()
    title = scrapy.Field()
    detail_url = scrapy.Field()
    model_id = scrapy.Field()
