import scrapy


class TwittercrawlerSpider(scrapy.Spider):
    name = 'TwitterCrawler'
    allowed_domains = ['twitter.com']
    start_urls = ['http://twitter.com/']

    def parse(self, response):
        pass
