# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import urllib2
import json
import codecs
import MySQLdb
from scrapy.exceptions import DropItem

import ImageUtils

class SpidercoverPipeline(object):

    def __init__(self):
        self.file = codecs.open('data.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line.decode('unicode_escape'))
        return item


class DownloadCoverPipeline(object):

    def process_item(self, item, spider):
        formate = item['cover'][item['cover'].rindex('.'):]

        dirPath = 'cover/' + item['artist_name']
        filePath = 'cover/' + item['artist_name'] + '/' + item['album_name'] + formate

        if os.path.exists(filePath):
            raise DropItem("Duplicate item found: %s" % item['album_name'])
        else:
            if not os.path.exists(dirPath):
                os.makedirs(dirPath)

            f = urllib2.urlopen(item['cover']) 
            with open(filePath, "wb") as code:
                code.write(f.read()) 
                f.close()
                code.close()

            info = ImageUtils.get_image_info(filePath)

            item['cover_path'] = filePath
            item['cover_color'] = info[0]
            item['cover_width'] = info[1]
            item['cover_height'] = info[2]

            return item


class SaveCoverPipeline(object):

    def process_item(self, item, spider):
        try:
            sql = "SELECT * FROM `album_xiami` WHERE `album_id` = %s"
            self.cur.execute(sql, (item['album_id'],))

            data = self.cur.fetchone()

            if data:
                print 'already >>>'
            else:
                sql = "INSERT INTO `album_xiami` (`album_id`, `album_name`, `cover`, `cover_path`, `cover_color`, `cover_width`, `cover_height`, `artist_id`, `artist_name`, `artist_name2`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                self.cur.execute(sql, (item['album_id'], item['album_name'], item['cover'], item['cover_path'], item['cover_color'], item['cover_width'], item['cover_height'], item['artist_id'], item['artist_name'], item['artist_name2'],))
                self.conn.commit()

        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

        return item

    def open_spider(self, spider):
        self.conn = MySQLdb.connect(host='localhost',user='root',passwd='2238447',db='formater',port=3306,charset='utf8',use_unicode=True)
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
