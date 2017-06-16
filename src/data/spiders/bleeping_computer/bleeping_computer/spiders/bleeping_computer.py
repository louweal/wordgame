import scrapy
from scrapy.conf import settings

class WordsSpider(scrapy.Spider):
	name = "bleeping_computer" 
	
	custom_settings = { # scrape pages in order
		'DOWNLOAD_DELAY': 2, 
		'CONCURRENT_REQUESTS_PER_DOMAIN': 1
	}
	

	def start_requests(self):

		urls2 = []
		urls2.append('https://www.bleepingcomputer.com/forums/t/2351/forum-game-word-association-take-2/')
		for i in range(2, 256): #255
			urls2.append('https://www.bleepingcomputer.com/forums/t/2351/forum-game-word-association-take-2/page-'+str(i))

		urls3 = []
		urls3.append('https://www.bleepingcomputer.com/forums/t/22370/forum-game-word-association-take-3/')
		for i in range(2, 330): #329
			urls3.append('https://www.bleepingcomputer.com/forums/t/22370/forum-game-word-association-take-3/page-'+str(i))

		urls5 = [] #re-srcape!
		for i in range(1, 210): #209
			urls5.append('https://www.bleepingcomputer.com/forums/t/414463/forum-game-word-association-take-5/page-'+str(i))


		urls = urls3 # select topic
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		for item in response.xpath('//div[contains(@id,"post_id_")]'):
			word = item.xpath('normalize-space(div/div/div[contains(@class, "entry-content")]//text())').extract() 
			author = item.xpath('normalize-space(div/h3/span[contains(@class, "author")]/text())').extract_first()

			yield {
			'word': word,
			'author': author 
			}


