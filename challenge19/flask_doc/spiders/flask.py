# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from flask_doc.items import PageItem


class FlaskSpider(CrawlSpider):
    name = 'flask'
    allowed_domains = ['flask.pocoo.org']
    start_urls = ['http://flask.pocoo.org/docs/1.0/']

    rules = (
    	Rule(LinkExtractor(allow='http://flask.pocoo.org/docs/1.0/*'),callback='parse_page',follow=True),
    )


    def parse_page(self, response):
        url = response.url
        text = re.sub('\s+',' ',' '.join(response.xpath('//text()').extract()))
        item = PageItem(url=url, text=text)
        yield item

