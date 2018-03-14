import scrapy

from DY2018.items import Dy2018Item


class Dy2018Spider(scrapy.Spider):
    name = 'dy2018'
    allowed_domains = ['dy2018.com']
    start_urls = ['https://www.dy2018.com/html/gndy/dyzz/index.html']

    def parse(self, response):
        table_list = response.xpath("//table[@class='tbspan']")
        for table in table_list:
            item = Dy2018Item()
            item["title"] = table.xpath(".//td/b/a/text()").extract_first()
            item["update_date"] = table.xpath(".//td/font/text()").extract_first().split()[0].split("：")[-1]
            item["detail_url"] = "https://www.dy2018.com" + table.xpath(".//td/b/a/@href").extract_first()
            item["info"] = table.xpath("./tr[4]/td/text()").extract_first()
            # item["info"] = "".join(item["info"].split())
            yield scrapy.Request(
                item["detail_url"],
                callback=self.parse_detail,
                meta={"item": item}
            )
        next_url = response.xpath("//a[text()='下一页']/@href").extract_first()
        if next_url:
            next_url = "https://www.dy2018.com" + next_url
            yield scrapy.Request(
                next_url,
                callback=self.parse
            )

    def parse_detail(self, response):
        item = response.meta["item"]
        item["grade"] = response.xpath("//div[@class='position']/span[1]/strong/text()").extract_first()
        item["category"] = response.xpath("//div[@class='position']/span[2]//text()").extract()
        item["category"] = "".join(item["category"]).split("：")[-1]
        item["release_time"] = response.xpath("//div[@id='Zoom']/p[contains(text(),'上映日期')]/text()").extract_first()
        item["release_time"] = item["release_time"].split()[-1] if item["release_time"] else None
        item["img"] = response.xpath("//div[@id='Zoom']//p/img/@src").extract_first()
        item["thunder_list"] = response.xpath("//table/tbody/tr/td/a/text()").extract_first()
        # print(item)
        yield item
