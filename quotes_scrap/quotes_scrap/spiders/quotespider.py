import scrapy
import time


class QuotespiderSpider(scrapy.Spider):
    name = "quotespider"
   
   
    def start_requests(self):
        yield scrapy.Request( url ="https://quotes.toscrape.com/js/",
                             meta = {'playwright': True})
        

    def parse(self, response):
        for quote in response.xpath('//div[@class ="quote"]'):
            time.sleep(20)
        
            yield {
            
                    'Author' : quote.xpath('.//small[@class ="author"]//text()').get(),
                    'Description' : quote.xpath('.//span[@class="text"]//text()').get()
            
            }
