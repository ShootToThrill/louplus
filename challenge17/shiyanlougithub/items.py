# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShiyanlougithubItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    update_time = scrapy.Field()
    commits = scrapy.Field()
    branches = scrapy.Field()
    releases = scrapy.Field()
 #    name = Column(String(64))
	# update_time = Column(DateTime)
	# commits = Column(Integer)
	# branches = Column(Integer)
	# releases = Column(Integer)
