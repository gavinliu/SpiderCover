# -*- coding: utf-8 -*-

import scrapy

from SpiderCover.items import CoverItem
from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector

class BaseSpider(CrawlSpider):
    # 专辑详情页
    d_title = "/html/body/div[@id='page']/div[@id='wrapper']/div[@id='title']/h1/text()"
    d_cover = "/html/body/div[@id='page']/div[@id='wrapper']/div[@id='content']/div[@id='main_wrapper']/div[@id='main_content']/div[@id='main']/div[@id='album_block']/div[@id='album_cover']/a[@id='cover_lightbox']/@href"
    d_artist_name = "/html/body/div[@id='page']/div[@id='wrapper']/div[@id='content']/div[@id='main_wrapper']/div[@id='main_content']/div[@id='main']/div[@id='album_block']/div[@id='album_info']/table/tr[1]/td[2]/a[1]/text()"
    d_artist_name2 = "/html/body/div[@id='page']/div[@id='wrapper']/div[@id='content']/div[@id='main_wrapper']/div[@id='main_content']/div[@id='main']/div[@id='album_block']/div[@id='album_info']/table/tr[1]/td[2]/a[1]/@title"
    d_artist_url = "/html/body/div[@id='page']/div[@id='wrapper']/div[@id='content']/div[@id='main_wrapper']/div[@id='main_content']/div[@id='main']/div[@id='album_block']/div[@id='album_info']/table/tr[1]/td[2]/a[1]/@href"


class CoverSpider(BaseSpider):
    name = 'cover'
    allowed_domains = ['www.xiami.com']
    start_urls = ['http://www.xiami.com/artist/album/id/1260']

    rules = [Rule(LinkExtractor(allow=('album/[0-9]+', )), callback='parse_cover', process_request='add_cookie'),
             Rule(LinkExtractor(allow=('artist/album/[0-9]+', 'artist/album-[0-9]+', 'artist/[0-9]+', 'artist/album/id/[0-9]+' )), process_request='add_cookie'), ]

    def parse_cover(self, response):
        item = CoverItem()

        item['album_id'] = Selector(text=response.url).re('[0-9]+')[0]
        item['album_name'] = response.xpath(self.d_title).extract()[0]

        item['artist_id'] = response.xpath(self.d_artist_url).re('[0-9]+')[0]
        item['artist_name'] = response.xpath(self.d_artist_name).extract()[0]
        item['artist_name2'] = response.xpath(self.d_artist_name2).extract()[0]
 
        item['cover'] = response.xpath(self.d_cover).extract()[0]

        yield item

    def add_cookie(self, request):
        request.replace(cookies=[{'name': '_unsign_token','value': 'e2683a724c63ad16358ffc5376a3adbc','domain': '.xiami.com','path': '/'},
                                 {'name': '_xiamitoken','value': '3cc7c4eff51845b91479bd4e1b73b729','domain': '.xiami.com','path': '/'},
                                 {'name': 'member_auth','value': '1WuaG9wZ7W40iveVGNxjcHBKtOeHSDeOwd5WjL4osVd2JNgAa4f8lauSRw1N0CSRrGHLnA1JX4qZhmGFm3l1fBKyHg','domain': '.xiami.com','path': '/'},
                                 ]);
        return request;
