import scrapy
from scrapy.conf import settings

class WordsSpider(scrapy.Spider):
	name = "pinkbike" 
	
	custom_settings = {
		'DOWNLOAD_DELAY': 2, 
		'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
		'ROBOTSTXT_OBEY': False
	}
	

	def start_requests(self):
		urls = []
		for i in range(1, 2748): #2747
			urls.append('https://www.pinkbike.com/forum/listcomments/?threadid=107062&pagenum='+str(i))

		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		for item in response.xpath('//div[contains(@id,"commentid")]'):
			word = item.xpath('normalize-space(table/tr/td[@class="forum-message"]/table/tr/td[@class="padding10"]/text())').extract() 
			author = item.xpath('normalize-space(table/tr/td/div[contains(@class,"forum-author2")]/div/a/text())').extract_first()

			yield {
			'word': word,
			'author': author 
			}


