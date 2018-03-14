# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class OnejavItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    thumb = scrapy.Field()
    detail_url = scrapy.Field()
    produce_date= scrapy.Field()
    actress_name = scrapy.Field()
    actress_url = scrapy.Field()
    torrent = scrapy.Field()
    size = scrapy.Field()
    similar_url_list = scrapy.Field()
    similar_img_list = scrapy.Field()
