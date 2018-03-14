# -*- coding: utf-8 -*-
import scrapy

from DYTT8.items import Dytt8Item


class Dytt8Spider(scrapy.Spider):
    name = 'dytt8'
    allowed_domains = ['dytt8.net']
    start_urls = ['http://www.dytt8.net/html/gndy/dyzz/list_23_2.html']
    # start_urls = ['http://www.dytt8.net/html/gndy/china/list_4_1.html']

    def parse(self, response):
        table_list = response.xpath("//div[@class='co_content8']/ul/td/table")
        for table in table_list:
            item = Dytt8Item()
            item["title"] = table.xpath("./tr[2]/td[2]/b/a/text()").extract_first()
            item["detail_url"] = "http://www.dytt8.net" + table.xpath("./tr[2]/td[2]/b/a/@href").extract_first()
            item["update_date"] = table.xpath("./tr[3]/td[2]/font/text()").extract_first().split("\n")[0]
            item["info"] = table.xpath("./tr[4]/td/text()").extract_first()
            yield scrapy.Request(
                item["detail_url"],
                callback=self.parse_detail_page,
                meta={"item": item}
            )

    def parse_detail_page(self, response):
        item = response.meta["item"]
        item["thunder"] = response.xpath("//table/tbody/tr/td/a/text()").extract_first()
        print(item)
        print("="*80)