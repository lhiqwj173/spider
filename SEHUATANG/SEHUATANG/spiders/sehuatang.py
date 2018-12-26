# -*- coding: utf-8 -*-
import scrapy
from SEHUATANG.items import SehuatangItem

class SehuatangSpider(scrapy.Spider):
    name = 'sehuatang'
    allowed_domains = ['sehuatanglu.com']
    start_urls = ['http://sehuatanglu.com/forum.php?mod=forumdisplay&fid=2&mobile=2']

    def parse(self, response):
        div_list = response.xpath("//div[contains(@class,'ztyzjj')]")
        for div in div_list:
            item = SehuatangItem()
            item["title"] = div.xpath(".//a/text()").extract_first()
            item["detail_url"] = "http://sehuatanglu.com/" + div.xpath(".//a/@href").extract_first()
            # 提取详情页信息
            yield scrapy.Request(
                item["detail_url"],
                callback=self.parse_detail_page,
                meta={"item": item}
            )
        # todo 翻页
        next_url = response.xpath("//a[text()='下一页']/@href").extract_first()
        if next_url:
            next_url = "http://sehuatanglu.com/" + next_url
            yield scrapy.Request(
                next_url,
                callback=self.parse
            )

    def parse_detail_page(self, response):
        item = response.meta["item"]
        message = response.xpath("//div[@class='message']//text()").extract()
        message = [x.strip() for x in message if "【" in x]
        for msg in message:
            if "【影片名称】" in msg:
                item["title"] = msg.split("：")[-1]
            if "【影片大小】" in msg:
                item["size"] = msg.split("：")[-1]
        img = response.xpath("//div[@class='message']//a[@class='orange']/@href").extract_first()
        item["img_list"] = "http://sehuatanglu.com/" + img if img else img
        # item["img_list"]  = [x for x in img_list if x.xpath("./id")]
        item["blockcode"] = response.xpath("//div[@class='blockcode']//text()").extract_first()
        print(response.url, "已经处理完毕")
        yield item
