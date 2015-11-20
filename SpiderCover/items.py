# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CoverItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    album_id = scrapy.Field()
    album_name = scrapy.Field()
    cover = scrapy.Field()
    cover_path = scrapy.Field()
    cover_color = scrapy.Field()
    cover_width = scrapy.Field()
    cover_height = scrapy.Field()
    
    artist_id = scrapy.Field()
    artist_name = scrapy.Field()
    artist_name2 = scrapy.Field()


