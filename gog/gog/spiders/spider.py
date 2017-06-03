import scrapy


class QuotesSpider(scrapy.Spider):
	name = "gog"
 
	def start_requests(self):
        	urls = []
    		for i in range(251, 301):
    			urls.append('https://www.gog.com/forum/general/word_association_game/page'+str(i))
    			
    		for url in urls:
    			yield scrapy.Request(url=url, callback=self.parse)
        
    	def parse(self, response):
        	for item in response.css('div.post_text'):
        		yield {
        			'word': item.css('div.post_text_c::text').extract()
		}


