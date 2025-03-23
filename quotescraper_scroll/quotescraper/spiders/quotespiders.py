import scrapy


class QuotespidersSpider(scrapy.Spider):
    name = "quotespiders"
    allowed_domains = ["xx"]
    start_urls = ["https://xx"]

    def parse(self, response):
        pass
