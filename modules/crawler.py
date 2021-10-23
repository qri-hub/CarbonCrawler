import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
class Crawler(CrawlSpider):
    name ="crawler"
    custom_settings = {'DOWNLOAD_DELAY' : 1}

    def __init__(self, domain, storepath):
        super().__init__()    
        self.allowed_domains = [domain]
        self.start_urls = ['http://'+domain]
        self.storepath = storepath

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def start_requests(self):
        print('started')
        yield scrapy.Request(url)

    def parse_item(self, response):
        filename = response.url.split("/")[-2] + '.html'
        with open(self.storepath+filename, 'wb') as f:
            f.write(response.body)