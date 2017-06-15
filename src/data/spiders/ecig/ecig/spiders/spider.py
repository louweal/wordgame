import scrapy
#from scrapy.selector import Selector
#from scrapy.http import HtmlResponse

class WordsSpider(scrapy.Spider):
	name = "ecig" 

	custom_settings = {
		'DOWNLOAD_DELAY': 2, 
		'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
	}

	def start_requests(self):
		urls1 = []
		urls1.append('http://www.e-cigarette-forum.com/forum/threads/word-association-game.142036/')
		for i in range(2, 404): #403
			urls1.append('http://www.e-cigarette-forum.com/forum/threads/word-association-game.142036/page-'+str(i))


		urls2 = []
		urls2.append('http://www.e-cigarette-forum.com/forum/threads/word-association-game-part-2.293399/')
		for i in range(2, 778): #777
			urls2.append('http://www.e-cigarette-forum.com/forum/threads/word-association-game-part-2.293399/page-'+str(i))


		urls3 = []
		urls3.append('http://www.e-cigarette-forum.com/forum/threads/word-association-game-part-3.622220/')
		for i in range(2, 331): #330
			urls3.append('http://www.e-cigarette-forum.com/forum/threads/word-association-game-part-3.622220/page-'+str(i))

		urls = urls3 # select topic to scrape
		
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		for item in response.xpath('//li[contains(@id,"post-")]'):
			word = item.xpath('normalize-space(div/div[@class="messageContent"]/article/blockquote//text())').extract() 
			author = item.xpath('div/div/h3/a//text()').extract_first()
			yield {
			'word': word,
			'author': author 
			}
