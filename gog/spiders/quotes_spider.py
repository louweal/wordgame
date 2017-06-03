import scrapy


class QuotesSpider(scrapy.Spider):
	name = "wag" #this name is used to run the spiders

	def start_requests(self):
        	urls = []
    		for i in range(1, 5033):
    			urls.append('https://www.gog.com/forum/general/word_association_game/page'+str(i))
    			
    		for url in urls:
    			yield scrapy.Request(url=url, callback=self.parse)
        
    	def parse(self, response):
        	for item in response.css('div.post_text'):
        		yield {
        			'word': item.css('div.post_text_c::text').extract()
		}


