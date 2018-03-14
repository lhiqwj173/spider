# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Dy2018Item(scrapy.Item):
    title = scrapy.Field()
    update_date = scrapy.Field()
    detail_url = scrapy.Field()
    info = scrapy.Field()
    grade = scrapy.Field()
    category = scrapy.Field()
    release_time = scrapy.Field()
    img = scrapy.Field()
    thunder_list = scrapy.Field()


