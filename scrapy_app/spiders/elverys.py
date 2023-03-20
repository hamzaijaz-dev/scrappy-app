import scrapy


def get_price(products):
    if products.css('div.prdt-price::text').get().replace('€', '').replace('\n', ''):
        return products.css('div.prdt-price::text').get().replace('€', '').replace('\n', '')
    else:
        return products.css('span.was-price::text').get().replace('€', '').replace('\n', '')


class ElverysSpider(scrapy.Spider):
    name = 'elverys'
    allowed_domains = ['https://www.elverys.ie/']
    start_urls = ['https://www.elverys.ie/Elverys/Men/Footwear/Running/c/2515?cat=Men']

    def parse(self, response):
        for products in response.css('div.product-box.grid-prdt'):
            yield {
                'name': products.css('a.text-transform-none.prdt-name::text').get(),
                'price': get_price(products),
                'link': 'https://www.elverys.ie' + products.css('a.prdt-img').attrib['href']
            }
