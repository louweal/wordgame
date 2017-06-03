import scrapy


class WordsSpider(scrapy.Spider):
	name = "learn-english" #this name is used to run the spiders

	def start_requests(self):
        	urls = []
		for i in range(1, 4):
			urls.append('http://learn-english-forum.org/discussion/13/word-association/p'+str(i))
			
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)
        
	def parse(self, response):
         for item in response.css('div.Comment'):
            word = item.css('div.Message::text').extract_first()
            word = word.replace("\n","")
            #do reg.ex replace trailing spaces 
            author = item.css('a.Username::text').extract_first() 
            yield {
            'word': word,
            'author': author 
            }
