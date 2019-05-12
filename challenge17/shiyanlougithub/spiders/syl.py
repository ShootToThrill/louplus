# -*- coding: utf-8 -*-
from scrapy import Spider, Request

from shiyanlougithub.items import ShiyanlougithubItem


class SylSpider(Spider):
    name = 'syl'
    url = 'https://github.com/shiyanlou?tab=repositories'
    def start_requests(self):
        while self.url:
            yield Request(url=self.url, callback=self.parse)

    def parse(self, response):
        repositories_list = response.css('div#user-repositories-list')

        self.url = repositories_list.css('div.BtnGroup')\
                    .xpath('./*[contains(@class,"BtnGroup-item")][2]/@href')\
                    .extract_first()

        repositories_items = repositories_list.xpath('./ul/li')

        for item in repositories_items:

            repositories_name = item.css('a[itemprop="name codeRepository"]::text')\
                                .re_first('[^\S]*(\S+)[^\S]*')
            repositoriy_href =  response.urljoin(item.css('a[itemprop="name codeRepository"]::attr(href)')\
                                .extract_first())

            repositories_update_time = item.css('relative-time::attr(datetime)').extract_first()

            item = ShiyanlougithubItem({
                'name' : repositories_name,
                'update_time': repositories_update_time
            })

            request = Request(url=repositoriy_href,callback=self.detail_parse)
            request.meta['item'] = item

            yield request

    def detail_parse(self, response):
    	item = response.meta['item']
    	item['commits'] = response.css('ul.numbers-summary li.commits span.num::text').extract_first().strip()
    	item['branches'] = response.css('ul.numbers-summary').xpath('./li[2]').css('span.num::text').extract_first().strip()
    	item['releases'] = response.css('ul.numbers-summary').xpath('./li[3]').css('span.num::text').extract_first().strip()
    	yield item

