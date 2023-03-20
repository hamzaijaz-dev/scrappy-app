import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule


class LalalandSpider(scrapy.Spider):
    name = 'lalaland'
    allowed_domains = ['https://www.lalaland.pk/']
    start_urls = ['https://www.lalaland.pk/mens-coats-jackets']
    Rules = (Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@class="page-link"]',)), callback="parse", follow= True),)

    def parse(self, response):
        for products in response.css('div.card.product_card'):
            if products.css('h4.bd_name::text').get() is not None:
                yield {
                    'brand': products.css('h4.bd_name::text').get(),
                    'name': products.css('h5.card-title::text').get(),
                    'price': products.css('span.price_heighlite::text').get()
                }

        # pick first element always : 'javascript:void(0)'
        # next_page = response.css('a.page-link').attrib['href']
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)

        # follow next page links
        next_page = response.xpath('.//a[@class="page-link"]/@href').extract()
        if next_page:
            next_href = next_page[1]
            next_page_url = 'https://www.lalaland.pk/mens-coats-jackets?page=' + next_href
            request = scrapy.Request(url=next_page_url)
            yield request
