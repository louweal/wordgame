import scrapy

class WordsSpider(scrapy.Spider):
	name = "classic_comics" 
	
	custom_settings = { 
		'DOWNLOAD_DELAY': 2, 
		'CONCURRENT_REQUESTS_PER_DOMAIN': 1, # scrape pages in given order
	}

	def start_requests(self):
		urls = []
		for i in range(1, 615): #614
			urls.append('http://classiccomics.org/thread/1234/word-association-game?page='+str(i))


		urls = urls 
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		for item in response.xpath('//tr[contains(@id,"post-")]'):
			print(item)
			word = ''.join(item.xpath('td/table/tr/td/article/div[contains(@class,"message")]//text()').extract())
			author = item.xpath('td/table/tr/td/div[@class="mini-profile"]/a/text()').extract_first() 
			yield {
			'word': word,
			'author': author 
			}
