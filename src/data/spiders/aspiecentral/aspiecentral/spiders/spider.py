import scrapy
#from scrapy.selector import Selector
#from scrapy.http import HtmlResponse

class WordsSpider(scrapy.Spider):
	name = "aspiecentral" 

	def start_requests(self):
		urls = []
		urls.append('https://www.aspiescentral.com/threads/word-association-game.86/')
		for i in range(2, 1153): #1152
			urls.append('https://www.aspiescentral.com/threads/word-association-game.86/page-'+str(i))

		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		for item in response.xpath('//li[contains(@id,"post-")]'):
			word = item.xpath('normalize-space(div/div/div[@class="messageContent"]/article/blockquote//text())').extract() 
			author = item.xpath('div/div/div/h3/a//text()').extract_first()
			yield {
			'word': word,
			'author': author 
			}
