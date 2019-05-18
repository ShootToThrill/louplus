import json 
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from scrapy.http import HtmlResponse



def parse_result():
	ret = []
	def parse(response):
		comments = response.css('div.course-comment div.comment-item')
		ret.extend([{'username':comment.css('div.user-name a.name::text').extract_first().strip(),\
			'content':comment.css('div.content::text').extract_first().strip()} for comment in comments])
		return ret
	return parse

parse = parse_result()

def has_next_page(response):
	# print(.xpath('./li[2]/@class'))
	if 'disabled' in response.css('ul.pagination').xpath('./li[2]/@class').extract_first():
		return False
	return True

def goto_next_page(driver):
	ac = driver.find_element_by_xpath('(//li[contains(@class, "page-item")])[2]')
	ActionChains(driver).move_to_element(ac).perform()
	time.sleep(2)
	ac.click()

def spider():
	driver = webdriver.Chrome()

	url = 'https://www.shiyanlou.com/courses/427'
	driver.get(url)
	ret = None
	while True:
		driver.implicitly_wait(5)
		html = driver.page_source
		response = HtmlResponse(url=url, body=html.encode('utf8'))
		ret = parse(response)
		if not has_next_page(response):
			break
		goto_next_page(driver)
	with open('/home/shiyanlou/comments.json', 'w') as f:
		f.write(json.dumps(ret))

if __name__ == '__main__':
	spider()