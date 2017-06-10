import scrapy


class WordsSpider(scrapy.Spider):
	name = "learn-english" 

	def start_requests(self):
        	urls = []
		for i in range(1, 220):
			urls.append('http://learn-english-forum.org/discussion/13/word-association/p'+str(i))
			
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)


        
	def parse(self, response):
         for item in response.css('div.Comment'):
            word = item.css('div.Message::text').extract_first()
            word = word.replace("\n","")
            author = item.css('a.Username::text').extract_first() 
            yield {
            'word': word,
            'author': author 
            }

	def parse(self, response):
		for item in response.xpath('//li[contains(@id,"Comment_")]'):
			word = item.xpath('normalize-space(div/div/div/div[@class="Message"]/text())').extract() 
			author = item.xpath('normalize-space(div/div/div/span/a[@class="Username")]/text())').extract_first()

			yield {
			'word': word,
			'author': author 
			}


