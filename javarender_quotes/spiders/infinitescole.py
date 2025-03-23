import scrapy
from scrapy_playwright.page import PageMethod
from javarender_quotes.items import JavarenderQuotesItem  # Ensure correct import of your item class


class InfinitescoleSpider(scrapy.Spider):
    name = "infinitescole"

    def start_requests(self):
        yield scrapy.Request(
            url="https://quotes.toscrape.com/scroll",
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[
                    PageMethod('wait_for_selector', 'div.quote'),
                    PageMethod("evaluate", 'window.scrollBy(0, document.body.scrollHeight)'),
                    PageMethod("wait_for_selector", "div.quote:nth-child(11)"),
                    PageMethod("evaluate", 'window.scrollBy(0, document.body.scrollHeight)'),
                    PageMethod("wait_for_selector", "div.quote:nth-child(21)"),
                    PageMethod("evaluate", 'window.scrollBy(0, document.body.scrollHeight)'),
                    PageMethod("wait_for_selector", "div.quote:nth-child(31)"),
                    PageMethod("evaluate", 'window.scrollBy(0, document.body.scrollHeight)'),
                    PageMethod("wait_for_selector", "div.quote:nth-child(41)"),
                    PageMethod("evaluate", 'window.scrollBy(0, document.body.scrollHeight)'),
                    PageMethod("wait_for_selector", "div.quote:nth-child(51)"),
                    PageMethod("evaluate", 'window.scrollBy(0, document.body.scrollHeight)'),
                    PageMethod("wait_for_selector", "div.quote:nth-child(61)"),
                    PageMethod("evaluate", 'window.scrollBy(0, document.body.scrollHeight)'),
                    PageMethod("wait_for_selector", "div.quote:nth-child(71)"),
                    PageMethod("evaluate", 'window.scrollBy(0, document.body.scrollHeight)'),
                    PageMethod("wait_for_selector", "div.quote:nth-child(81)"),
                    PageMethod("evaluate", 'window.scrollBy(0, document.body.scrollHeight)'),
                    PageMethod("wait_for_selector", "div.quote:nth-child(91)"),
                    
                ],
                errback=self.errback,
            ),
        )

    async def parse(self, response):
        page = response.meta['playwright_page']
        

        for quote in response.css('div.quote'):
            quote_item = JavarenderQuotesItem()
            quote_item['text'] = quote.css('span.text::text').get()
            quote_item['author'] = quote.css('small.author::text').get()
            quote_item['tags'] = quote.css('div.tags a.tag::text').getall()
            yield quote_item

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
