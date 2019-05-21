import csv
import asyncio
import aiohttp
import async_timeout
from scrapy.http import HtmlResponse

results = []

def parse(url, body):
    response = HtmlResponse(url=url, body=body, encoding='utf8')

    repositories_list = response.css('div#user-repositories-list')
    repositories_items = repositories_list.xpath('./ul/li')

    for item in repositories_items:

        repositories_name = item.css('a[itemprop="name codeRepository"]::text')\
                            .re_first('[^\S]*(\S+)[^\S]*')

        repositories_update_time = item.css('relative-time::attr(datetime)').extract_first()

        results.append((repositories_name, repositories_update_time))

async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()


async def task(url):
    async with aiohttp.ClientSession() as session:
        body = await fetch(session, url)
        parse(url,body)

def main():
    loop = asyncio.get_event_loop()
    urls = [
        'https://github.com/shiyanlou?tab=repositories',
        'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNy0wNi0wN1QwODowMTo1NyswODowMM4FkpUr&tab=repositories',
        'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNS0wMS0yOFQwOTozMDowMSswODowMM4ByPC5&tab=repositories',
        'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNC0xMS0yNFQxOToxNjoxMiswODowMM4BnYLL&tab=repositories',
        'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNC0wNy0wNFQxMzoyMDowOSswODowMM4BR9ql&tab=repositories', 
    ]
    tasks = [ task(url) for url in urls]
    loop.run_until_complete(asyncio.gather(*tasks))
    print(results)
    with open('/home/shiyanlou/shiyanlou-repos.csv','w',newline='') as f:
        writer = csv.writer(f)
        writer.writerows(results)

if __name__ == '__main__':
    main()
