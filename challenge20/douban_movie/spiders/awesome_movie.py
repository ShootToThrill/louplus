# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from douban_movie.items import MovieItem


class AwesomeMovieSpider(CrawlSpider):
    name = 'awesome-movie'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/subject/3011091/']

    rules = (
    	Rule(LinkExtractor(allow=r"https://movie.douban.com/subject/.+/?from=subject-page"), follow=True, callback="parse_page"),
    )

    def parse_movie_item(self, response):
        score_str = response.css('div.rating_self strong.rating_num::text').extract_first()
        try:
        	score = float(score_str)
        except ValueError:
        	print(score_str+'can not convert to float ')
        	score = 0

        if score >= 8:
        	url = response.url
        	name = response.xpath('//span[@property="v:itemreviewed"]/text()').extract_first()
        	summary = response.xpath('//span[@property="v:summary"]/text()').extract_first()
        	item = MovieItem(score=score, url=url, name=name, summary=summary)

        	return item

    def parse_start_url(self, response):
        yield self.parse_movie_item(response)


    def parse_page(self, response):
        yield self.parse_movie_item(response)

