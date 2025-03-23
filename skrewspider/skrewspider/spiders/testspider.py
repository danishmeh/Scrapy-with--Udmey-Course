import scrapy


class TestspiderSpider(scrapy.Spider):
    name = "testspider"
    allowed_domains = ["www.kickscrew.com"]
    start_urls = ["https://www.kickscrew.com/collections/air-jordan"]

    def parse(self, response):
        pass
