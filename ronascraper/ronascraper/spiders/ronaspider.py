# from scrapy.utils.request import request_fingerprint
# from scrapy.http import Request
import scrapy

class RonaspiderSpider(scrapy.Spider):
    name = "ronaspider"
    allowed_domains = ["www.rona.ca"]
    start_urls = [
        "https://www.rona.ca/en/tools/power-tools-158001/cordless-power-tool-sets-158002"
    ]

    def parse(self, response):
        # Extract product holders
        holders = response.css('div.js-product-tile')
        
        for holder in holders:
            # Extract relative URL and construct full URL
            relative_url = holder.css("a.product-tile__image-link.productLink::attr(href)").get()
            
            yield scrapy.Request(relative_url, callback=self.parse_product)
        
        # Pagination logic: Follow the next page
        next_page_url = response.css('a.pagination__button-arrow--next::attr(href)').get()
        if next_page_url:
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_product(self, response):
        # Extract title and other details
        title = response.css('h1.page-product__title::text').get()
        if title:
            title = title.strip()

        article_number = response.css('div.page-product__sku-infos span::text').re_first(r'Article #(\d+)')
        item_number = response.css('div.page-product__sku-infos span::text').re_first(r'Item #(\d+)')
        model_number = response.css('div.page-product__sku-infos span::text').re_first(r'Model #(.*)')
        format = response.css('div.page-product__sku-infos span::text').re_first(r'Format (.*)')
        price = response.css('span.price-box__price__amount__integer::text').get()
        
        upc = response.css('script::text').re_first(r"var upcNumberWithPad\s*=\s*'(\d{12})'")


        # Yield the extracted data
        yield {
            'url': response.url,
            'title': title,
            'article_number': article_number,
            'item_number': item_number,
            'model_number': model_number,
            'format': format,
            'price': price,
            'upc': upc
        }
