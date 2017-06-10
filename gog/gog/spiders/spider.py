import scrapy

class QuotesSpider(scrapy.Spider):
	name = "gog"

	custom_settings = {
		'DOWNLOAD_DELAY': 2, 
		'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
	}

	def start_requests(self):
		urls = []
		for i in range(5001, 5055): #5054
			urls.append('https://www.gog.com/forum/general/word_association_game/page'+str(i))
		
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)


	def parse(self, response):
		for item in response.css('div.big_post_main'):
			yield {
				'word': item.css('div.post_text_c::text').extract(),
				'author' : item.css('div.b_u_name::text').extract_first()
			}
