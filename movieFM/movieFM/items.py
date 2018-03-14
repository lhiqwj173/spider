# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MoviefmItem(scrapy.Item):
    # define the fields for your item here like:
    number = scrapy.Field()
    name = scrapy.Field()
    year = scrapy.Field()
    type = scrapy.Field()
    director = scrapy.Field()
    grade = scrapy.Field()
