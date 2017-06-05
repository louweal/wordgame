import scrapy
#from scrapy.selector import Selector
#from scrapy.http import HtmlResponse

class WordsSpider(scrapy.Spider):
	name = "ecig" 

	def start_requests(self):
		urls = []
		urls.append('http://www.e-cigarette-forum.com/forum/threads/word-association-game.142036/')
		for i in range(2, 404): #403
			urls.append('http://www.e-cigarette-forum.com/forum/threads/word-association-game.142036/page-'+str(i))

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
