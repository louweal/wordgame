import scrapy
from scrapy.conf import settings

class WordsSpider(scrapy.Spider):
	name = "bleeping_computer" 
	
	custom_settings = { # scrape pages in order
		'DOWNLOAD_DELAY': 2, 
		'CONCURRENT_REQUESTS_PER_DOMAIN': 1
	}
	

	def start_requests(self):
		urls1 = []
		urls1.append('https://www.bleepingcomputer.com/forums/t/1752/forum-game-word-association/')
		for i in range(2, 73): #72
			urls1.append('https://www.bleepingcomputer.com/forums/t/1752/forum-game-word-association/page-'+str(i))

		urls2 = []
		urls2.append('https://www.bleepingcomputer.com/forums/t/2351/forum-game-word-association-take-2/')
		for i in range(2, 256): #255
			urls2.append('https://www.bleepingcomputer.com/forums/t/2351/forum-game-word-association-take-2/page-'+str(i))

		urls3 = []
		urls3.append('https://www.bleepingcomputer.com/forums/t/22370/forum-game-word-association-take-3/')
		for i in range(2, 330): #329
			urls3.append('https://www.bleepingcomputer.com/forums/t/22370/forum-game-word-association-take-3/page-'+str(i))

		urls4 = []
		urls4.append('https://www.bleepingcomputer.com/forums/t/194701/forum-game-word-association-take-4/')
		for i in range(2, 73): #72
			urls4.append('https://www.bleepingcomputer.com/forums/t/194701/forum-game-word-association-take-4/page-'+str(i))

		urls5 = []
		urls5.append('https://www.bleepingcomputer.com/forums/t/414463/forum-game-word-association-take-5/')
		for i in range(2, 210): #209
			urls5.append('https://www.bleepingcomputer.com/forums/t/414463/forum-game-word-association-take-5/page-'+str(i))

		urls6 = []
		urls6.append('https://www.bleepingcomputer.com/forums/t/486650/forum-game-word-association-take-6/')
		for i in range(2, 202): #201
			urls6.append('https://www.bleepingcomputer.com/forums/t/486650/forum-game-word-association-take-6/page-'+str(i))

		urls7 = []
		urls7.append('https://www.bleepingcomputer.com/forums/t/569699/forum-game-word-association-take-7/')
		for i in range(2, 248): #247
			urls7.append('https://www.bleepingcomputer.com/forums/t/569699/forum-game-word-association-take-7/page-'+str(i))
	
		urls = urls1 + urls2 + urls3 + urls4 + urls5 + urls6 + urls7 
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		for item in response.xpath('//div[contains(@id,"post_id_")]'):
			word = ''.join(item.xpath('div/div[@class="post_body"]/div[@itemprop="commentText"]//text()[not(ancestor::blockquote)]').extract())
			word = word.replace("\n", '')
			word = word.replace("\t", '')
			word = word.replace("\r", '')			
			author = item.xpath('normalize-space(div/h3/span[contains(@class, "author")]/text())').extract_first()

			yield {
			'word': word,
			'author': author 
			}


