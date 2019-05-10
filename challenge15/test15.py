from scrapy import Spider,Request

# repositories_list = response.css('div#user-repositories-list')

# next_page_href = repositories_list.css('div.BtnGroup')\
# .xpath('./*[contains(@class,"BtnGroup-item")][2]/@href')\
# .extract_first()

# repositories_items = repositories_list.xpath('./ul/li')
# repositories_name = repositories_items[0].css('a[itemprop="name codeRepository"]::text')
# .re_first('[^\S]*(\S+)[^\S]*')
# repositories_update_time = repositories_items[0].css('relative-time::attr(datetime)').extract()

class ShiyanlouRepoSpider(Spider):
	name = 'ShiyanlouRepo'
	url = 'https://github.com/shiyanlou?tab=repositories'

	def start_requests(self):
		while self.url:
			yield Request(self.url, callback=self.parse)

	def parse(self, response):
		repositories_list = response.css('div#user-repositories-list')

		self.url = repositories_list.css('div.BtnGroup')\
		.xpath('./*[contains(@class,"BtnGroup-item")][2]/@href')\
		.extract_first()

		repositories_items = repositories_list.xpath('./ul/li')

		for item in repositories_items:

			repositories_name = item.css('a[itemprop="name codeRepository"]::text')\
			.re_first('[^\S]*(\S+)[^\S]*')

			repositories_update_time = item.css('relative-time::attr(datetime)').extract_first()

			yield {
				'name' : repositories_name,
				'update_time': repositories_update_time
			}

