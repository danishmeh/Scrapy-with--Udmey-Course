import scrapy


class LazadaspiderSpider(scrapy.Spider):
    name = "lazadaspider"
    # allowed_domains = ["www.lazada.com"]
    # start_urls = ["https://www.lazada.com/en/contacts/"]

    def start_requests(self):
        yield scrapy.Request( 
                            url ="https://www.lazada.com.my/tag/best-gaming-laptop/",
                            meta ={"playwright": True})
    def parse(self, response):
        for p in response.xpath('//div[@class="_17mcb"]//div[@class="Bm3ON"]'):
        
            yield {
            
            "Title" : p.xpath('.//div[@class="RfADt"]//a//text()').get(),
            "Price" : p.xpath('.//div[@class="aBrP0"]//span[@class="ooOxS"]//text()').get(),
            "Page_URL" : response.url,
       
            
        }
