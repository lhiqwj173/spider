# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SehuatangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    detail_url = scrapy.Field()
    message = scrapy.Field()
    img_list = scrapy.Field()
    blockcode = scrapy.Field()
    size = scrapy.Field()
