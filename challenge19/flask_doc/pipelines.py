# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import redis

class FlaskDocPipeline(object):
    def process_item(self, item, spider):
        self.redis.lpush('flask_doc:items',json.dumps(dict(item)))
        # print(json.dumps(item))
        return item

    def open_spider(self,spider):
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)


