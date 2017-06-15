import scrapy
from scrapy.conf import settings

class WordsSpider(scrapy.Spider):
	name = "the_fishy" 
	
	custom_settings = { #scrape pages sequentially
		'DOWNLOAD_DELAY': 2, 
		'CONCURRENT_REQUESTS_PER_DOMAIN': 1, 
	}
	

	def start_requests(self):
		urls = []
		for i in range(0, 4060): #4060
			urls.append('http://forum.thefishy.co.uk/cgi-bin/forum/Blah.pl?m-1261668481/s-'+str(i*10))

		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		words = []
		authors = []
		for item in response.xpath('//table[contains(@class,"postbody")]'):
			words.append(item.xpath('normalize-space(tr/td/div[contains(@id,"m")]/text())').extract()) 

		for item in response.xpath('//td[contains(@class,"win center")]'):
			authors.append(item.xpath('normalize-space(strong//text())').extract_first())
			
		for i in range(0,len(authors)):
			yield {
			'word': words[i],
			'author': authors[i] 
			}


