# -*- coding: utf-8 -*-
import scrapy

from movieFM.items import MoviefmItem


class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['dianying.fm']
    off = 1
    temp_url = 'http://dianying.fm/collection/60655/?p={}'
    start_urls = [temp_url.format(off)]

    def parse(self, response):
        tr_list = response.xpath("//tr")
        # 数据解析
        item = MoviefmItem()
        for tr in tr_list[1:]:
            item['number'] = tr.xpath("./td[1]/text()").extract_first().strip().replace("#", "")
            item['name'] = tr.xpath("./td[2]/a/text()").extract_first().strip()
            item['year'] = tr.xpath("./td[3]/text()").extract_first().strip()
            item['type'] = tr.xpath("./td[4]/text()").extract_first().replace(" ", "")
            item['director'] = tr.xpath("./td[5]/text()").extract_first().strip()
            gread_list = tr.xpath("./td[6]/span//text()").extract()
            item['grade'] = "".join("".join(gread_list).split())
            yield item

        # 翻页
        self.off += 1
        next_url = self.temp_url.format(self.off)
        if self.off < 14:
            yield scrapy.Request(next_url)