import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

class WordsSpider(scrapy.Spider):
	name = "wrongplanet" 

	custom_settings = { #scrape pages sequentially
		'DOWNLOAD_DELAY': 2, 
		'CONCURRENT_REQUESTS_PER_DOMAIN': 1, 
	}

	def start_requests(self):
		urls = []
		for i in range(1001, 3826): #3825
			urls.append('http://wrongplanet.net/forums/viewtopic.php?f=30&t=9093&start='+str(15*i))

		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		for item in response.xpath('//div[@class="row"]'):
			print(item)
			word = item.xpath('div[@class="message-col"]/div[@class="message-content"]/p/text()').extract()
			author = item.xpath('div[@class="user-col"]/p/a/text()').extract_first() 
			yield {
			'word': word,
			'author': author 
			}
