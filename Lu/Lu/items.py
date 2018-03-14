# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LuItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    title = scrapy.Field()
    vmtype = scrapy.Field()
    linkurl = scrapy.Field()
    thumb = scrapy.Field()
    img_list = scrapy.Field()
    thunder = scrapy.Field()
    produceyear = scrapy.Field()
