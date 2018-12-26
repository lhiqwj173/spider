# -*- coding: utf-8 -*-
import scrapy
from MeiTuLu.items import MeituluItem

CATEGORY_URL_LIST = [
    'https://www.meitulu.com/t/toutiaonvshen/',
    'https://www.meitulu.com/t/nvshen/',
    'https://www.meitulu.com/t/jipin/',
    'https://www.meitulu.com/t/nenmo/',
    'https://www.meitulu.com/t/wangluohongren/',
    'https://www.meitulu.com/t/fengsuniang/',
    'https://www.meitulu.com/t/qizhi/',
    'https://www.meitulu.com/t/youwu/',
    'https://www.meitulu.com/t/baoru/',
    'https://www.meitulu.com/t/xinggan/',
    'https://www.meitulu.com/t/youhuo/',
    'https://www.meitulu.com/t/meixiong/',
    'https://www.meitulu.com/t/shaofu/',
    'https://www.meitulu.com/t/changtui/',
    'https://www.meitulu.com/t/mengmeizi/',
    'https://www.meitulu.com/t/loli/',
    'https://www.meitulu.com/t/keai/',
    'https://www.meitulu.com/t/huwai/',
    'https://www.meitulu.com/t/bijini/',
    'https://www.meitulu.com/t/qingchun/',
    'https://www.meitulu.com/t/weimei/',
    'https://www.meitulu.com/t/qingxin/',
    "https://www.meitulu.com/rihan/",
    "https://www.meitulu.com/gangtai/",
    "https://www.meitulu.com/guochan/"
]


class MeituluSpider(scrapy.Spider):
    name = 'meitulu'
    allowed_domains = ['www.meitulu.com']
    start_urls = CATEGORY_URL_LIST

    def parse(self, response):
        li_list = response.xpath("//ul[@class='img']/li")
        for li in li_list:
            item = MeituluItem()
            item["category"] = response.url.split("/")[-2]
            item["img_nums"] = int(li.xpath("./p[1]/text()").extract_first().split(" ")[1])
            model_name = li.xpath("./p[3]//text()").extract()
            item["model_name"] = "".join(model_name).split("：")[-1].strip()
            item["labels"] = "_".join(li.xpath("./p[4]/a/text()").extract())
            item["title"] = li.xpath("./p[@class='p_title']/a/text()").extract_first()
            item["detail_url"] = li.xpath("./p[@class='p_title']/a/@href").extract_first()
            model_id = item["detail_url"].replace(".html", "").split("/")[-1]
            item["model_id"] = model_id
            yield item

        next_page_url = response.xpath("//a[text()='下一页']/@href").extract_first()
        if next_page_url:
            if "meitulu" not in next_page_url:
                next_page_url = "https://www.meitulu.com" + next_page_url
            if next_page_url != response.url:
                print(next_page_url)
                yield scrapy.Request(
                    next_page_url,
                    callback=self.parse
                )
