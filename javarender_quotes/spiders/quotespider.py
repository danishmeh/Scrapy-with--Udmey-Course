import scrapy
from scrapy_playwright.page import PageMethod
from javarender_quotes.items import JavarenderQuotesItem # Ensure correct import of your item class

class QuotespiderSpider(scrapy.Spider):
    name = "quotespider"

    def start_requests(self):
        yield scrapy.Request(
            url="https://quotes.toscrape.com/js/",
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[PageMethod('wait_for_selector', 'div.quote')],
                errback=self.errback,
            ),
        )

    async def parse(self, response):
        page = response.meta['playwright_page']
        
        # The page will be closed automatically by the scrapy-playwright middleware
        # so you do not need to call await page.close() here.

        for quote in response.css('div.quote'):
            quote_item = JavarenderQuotesItem()
            quote_item['text'] = quote.css('span.text::text').get()
            quote_item['author'] = quote.css('small.author::text').get()
            quote_item['tags'] = quote.css('div.tags a.tag::text').getall()
            yield quote_item
            
        next_page = response.css('.next>a ::attr(href)').get()
        
        if next_page is not None:
            next_page_url = 'http://quotes.toscrape.com' + next_page 
            yield scrapy.Request(next_page_url,meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[PageMethod('wait_for_selector', 'div.quote')],
                errback=self.errback))

    def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        # The page will be closed automatically by the scrapy-playwright middleware
        # You don't need to call await page.close() in errback either.
