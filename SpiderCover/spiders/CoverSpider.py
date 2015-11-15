# -*- coding: utf-8 -*-

import scrapy

from SpiderCover.items import CoverItem
from scrapy.http import Request

class CoverSpider(scrapy.spiders.Spider):
    name = 'cover'
    allowed_domains = ['www.xiami.com']
    start_urls = ['http://www.xiami.com/album/1029065888?spm=0.0.0.0.ylCOkb']
    isFirst = True

    def parse(self, response):
        title = "/html/body/div[@id='page']/div[@id='wrapper']/div[@id='title']/h1/text()"
        coverXPATH = "/html/body/div[@id='page']/div[@id='wrapper']/div[@id='content']/div[@id='main_wrapper']/div[@id='main_content']/div[@id='main']/div[@id='album_block']/div[@id='album_cover']/a[@id='cover_lightbox']/@href"

        if self.isFirst:
            yield Request('http://www.xiami.com/album/166032', callback=self.parse)
            self.isFirst = False

        item = CoverItem()
        item['title'] = response.xpath(title).extract()
        item['cover'] = response.xpath(coverXPATH).extract()
        yield item
