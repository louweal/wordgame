import scrapy

class QuotesSpider(scrapy.Spider):
	name = "gog"

	def start_requests(self):
		urls = []
		for i in range(4001, 5001):
			urls.append('https://www.gog.com/forum/general/word_association_game/page'+str(i))
		
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)


	def parse(self, response):
		for item in response.css('div.big_post_main'):
			yield {
				'word': item.css('div.post_text_c::text').extract(),
				'author' : item.css('div.b_u_name::text').extract_first()
			}
