# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urljoin


class BusSpider(scrapy.Spider):
    name = 'bus'
    allowed_domains = ['javbus.com']
    start_urls = ['https://www.javbus.com/']

    def parse(self, response):
        item_list = response.xpath("//div[@id='waterfall']/div/a/@href").extract()

        for i in item_list:
            yield scrapy.Request(
                i,
                callback=self.parse_datial,
            )

        # 翻页
        next_page = response.xpath("//a[text()='下一頁']/@href").extract_first()
        if next_page is not None:
            yield scrapy.Request(
                urljoin("https://www.javbus.com", next_page),
                self.parse
            )

    def parse_datial(self, response):
        item = {}
        item["title"] = response.xpath("//h3/text()").extract_first()
        gid = response.xpath("//script/text()").re("var gid = (.*?);")[0]
        yield scrapy.Request(
            f"https://www.javbus.com/ajax/uncledatoolsbyajax.php?gid={gid}&lang=zh&uc=0",
            self.get_torrent,
            meta={"item": item}
        )

    def get_torrent(self, response):
        item = response.meta["item"]
        item["magnet"] = response.xpath("//tr/td/a/@href").extract_first()
        item["size"] = response.xpath("//tr/td[2]/a/text()").extract_first().strip()
        item["datetime"] = response.xpath("//tr/td[3]/a/text()").extract_first().strip()
        print(item)
        yield item
