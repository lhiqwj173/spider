# -*- coding: utf-8 -*-
import requests
import scrapy

from ONEJAV.items import OnejavItem
from ONEJAV.utils import gen_datetime


class OnejavSpider(scrapy.Spider):
    name = 'onejav'
    allowed_domains = ['onejav.com']
    # datetime_list = gen_datetime("2018/02/26")
    # start_urls = ['https://onejav.com/{}'.format(i) for i in datetime_list]

    start_urls = ['https://onejav.com/2018/03/09']

    def parse(self, response):
        div_list = response.xpath("//div[@class='columns']")
        print(len(div_list))
        for div in div_list:
            item = OnejavItem()
            item["thumb"] = div.xpath(".//img[@class='image']/@src").extract_first()
            item["title"] = div.xpath(".//h5[@class='title is-4 is-spaced']/a/text()").extract_first().split()[0]
            item["detail_url"] = "https://onejav.com" + div.xpath(
                ".//h5[@class='title is-4 is-spaced']/a/@href").extract_first()
            item["size"] = div.xpath(".//h5[@class='title is-4 is-spaced']/span/text()").extract_first().replace("\xa0",
                                                                                                                 "")
            item["produce_date"] = div.xpath(".//p[@class='subtitle is-6']/a/@href").extract_first()[1:]
            item["actress_name"] = div.xpath(".//a[@class='panel-block']/text()").extract()
            if len(item["actress_name"]) == 1:
                item["actress_name"] = item["actress_name"][0]
            elif len(item["actress_name"]) == 0:
                item["actress_name"] = None
            item["actress_url"] = div.xpath(".//a[@class='panel-block']/@href").extract()
            if len(item["actress_url"]) == 0:
                item["actress_url"] = None
            elif len(item["actress_url"]) == 1:
                item["actress_url"] = "https://onejav.com" + requests.utils.unquote(item["actress_url"][0])
            else:
                item["actress_url"] = ["https://onejav.com" + requests.utils.unquote(i) for i in item["actress_url"]]
            item["torrent"] = "https://onejav.com" + div.xpath(
                ".//a[contains(@class,'piwik_download')]/@href").extract_first()
            yield scrapy.Request(
                item["detail_url"],
                callback=self.parse_detail,
                meta={"item": item}
            )
        # 翻页
        next_url = response.xpath("//a[contains(@class,'pagination-next')]/@href").extract_first()
        if next_url:
            next_url = response.url.split("?")[0] + next_url
            yield scrapy.Request(
                next_url,
                callback=self.parse
            )

    def parse_detail(self, response):
        item = response.meta["item"]
        item["similar_img_list"] = response.xpath("//a[@class='thumbnail-link']/img/@src").extract()
        if not item["similar_img_list"]:
            item["similar_img_list"] = None
        item["similar_url_list"] = response.xpath("//a[@class='thumbnail-link']/@href").extract()
        if item["similar_url_list"]:
            item["similar_url_list"] = ["https://onejav.com" + i for i in item["similar_url_list"]]
        else:
            item["similar_url_list"] = None
        yield item
        # print(item)