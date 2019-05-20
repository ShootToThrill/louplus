# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import redis


class DoubanMoviePipeline(object):
    count = 0
    def process_item(self, item, spider):
        self.redis.lpush('douban_movie:items',json.dumps(dict(item)))
        self.count +=1
        if self.count >=30:
            spider.crawler.engine.close_spider(spider,'there is already 30 item and now stop!')
        print(json.dumps(dict(item)))
        return item

    def open_spider(self,spider):
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)
