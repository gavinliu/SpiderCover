# -*- coding: utf-8 -*-

import scrapy

from SpiderCover.items import CoverItem
from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

class BaseSpider(CrawlSpider):
    # 专辑详情页
    d_title = "/html/body/div[@id='page']/div[@id='wrapper']/div[@id='title']/h1/text()"
    d_cover = "/html/body/div[@id='page']/div[@id='wrapper']/div[@id='content']/div[@id='main_wrapper']/div[@id='main_content']/div[@id='main']/div[@id='album_block']/div[@id='album_cover']/a[@id='cover_lightbox']/@href"
    d_artist_name = "/html/body/div[@id='page']/div[@id='wrapper']/div[@id='content']/div[@id='main_wrapper']/div[@id='main_content']/div[@id='main']/div[@id='album_block']/div[@id='album_info']/table/tr[1]/td[2]/a/text()"
    d_artist_name2 = "/html/body/div[@id='page']/div[@id='wrapper']/div[@id='content']/div[@id='main_wrapper']/div[@id='main_content']/div[@id='main']/div[@id='album_block']/div[@id='album_info']/table/tr[1]/td[2]/a/@title"
    d_artist_url = "/html/body/div[@id='page']/div[@id='wrapper']/div[@id='content']/div[@id='main_wrapper']/div[@id='main_content']/div[@id='main']/div[@id='album_block']/div[@id='album_info']/table/tr[1]/td[2]/a/@href"

class CoverSpider(BaseSpider):
    name = 'cover'
    allowed_domains = ['www.xiami.com']
    start_urls = ['http://www.xiami.com/artist/1260']

    rules = [Rule(LinkExtractor(allow=('album/[0-9]+', )), callback='parse_cover'),
             Rule(LinkExtractor(allow=('artist/album/[0-9]+', 'artist/album-[0-9]+', 'artist/[0-9]+' ))), ]

    def parse_cover(self, response):

        item = CoverItem()
        item['title'] = response.xpath(self.d_title).extract()
        item['cover'] = response.xpath(self.d_cover).extract()
        item['artistName'] = response.xpath(self.d_artist_name).extract()
        item['artistName2'] = response.xpath(self.d_artist_name2).extract()
        item['artistID'] = response.xpath(self.d_artist_url).re('[0-9]+')[0]

        yield item
