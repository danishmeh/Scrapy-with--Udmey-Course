import scrapy

base = 'https://quotes.toscrape.com/api/quotes?page={}'
class ScrollspiderSpider(scrapy.Spider):
    name = "scrollspider"

    start_urls = [base.format(1)]

    def parse(self, response):
        data = response.json()
        
        for quote in data['quotes']:
            yield {
                
                'author' : quote['author']['name'],
                'text'  : quote['text']
            }
            
        current_page = data["page"]
        if data["has_next"]:
            next_page_url = base.format(current_page+1)
            yield scrapy.Request(next_page_url)