import json

import scrapy

from Lu.items import LuItem


class LuSpider(scrapy.Spider):
    name = 'lu'
    allowed_domains = ['555lu.vip']
    start_urls = ['https://m.555lu.vip/jsonvlist.php?classid={}&page=0'.format(i) for i in range(1, 14)]

    def parse(self, response):
        if response.text == '[]':
            return
        content_list = json.loads(response.text)
        for content in content_list:
            item = LuItem()
            item["id"] = content["id"]
            item["title"] = content["title"]
            item["linkurl"] = "https://m.555lu.vip/" + content["linkurl"]
            item["thumb"] = "https:" + content["thumb"]
            item["vmtype"] = content["vmtype"]
            item["produceyear"] = content["produceyear"]
            yield scrapy.Request(
                item["linkurl"],
                callback=self.parse_detail,
                meta={"item": item}
            )
        cur_page_number = int(response.url.split("=")[-1])
        next_url = "=".join(response.url.split("=")[:-1]) + "=" + str(cur_page_number + 1)
        print(next_url)
        yield scrapy.Request(
            next_url,
            callback=self.parse
        )

    def parse_detail(self, response):
        item = response.meta["item"]
        item["img_list"] = response.xpath("//div[@class='detailText']/p/img/@src").extract()
        item["img_list"] = ["https://" + i for i in item["img_list"]]
        item["thunder"] = response.xpath("//a[contains(text(),'迅雷下载')]/@href").extract_first()
        yield item
