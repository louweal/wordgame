import scrapy

class WordsSpider(scrapy.Spider):
	name = "sas" 

	
	custom_settings = {
		'DOWNLOAD_DELAY': 2, 
		'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
	}
	

	def start_requests(self):
		urls1 = []
		urls1.append("http://www.socialanxietysupport.com/forum/f31/word-association-19687/")
		for i in range(2, 2403): #2402
			urls1.append('http://www.socialanxietysupport.com/forum/f31/word-association-19687/index'+str(i)+".html")


		urls2 = []
		urls2.append("http://www.socialanxietysupport.com/forum/f31/word-association-2-a-494226/")
		for i in range(2, 686): #685
			urls2.append('http://www.socialanxietysupport.com/forum/f31/word-association-2-a-494226/index'+str(i)+".html")
		

		urls = urls1 + urls2 # select topic to scrape
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		for item in response.xpath('//section[contains(@id,"post")]'):
			print(item)
			word = ''.join(item.xpath('div/div/div/div[contains(@id,"post_message_")]//text()').extract())
			word = word.replace("\n", '')
			word = word.replace("\t", '')
			word = word.replace("\r", '')			
			author = item.xpath('div/div/div/a[contains(@class,"bigusername")]/text()').extract_first() 
			yield {
			'word': word,
			'author': author 
			}
