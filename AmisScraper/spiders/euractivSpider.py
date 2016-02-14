from AmisScraper.items import EuractivNewsItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule


class EuractivSpider(CrawlSpider):
    #log.start(logfile='~/log.txt', loglevel=log.CRITICAL)
    name = "euractiv"
    allowed_domains = ["www.euractiv.com"]
    start_urls = ["http://www.euractiv.com/sections/agriculture-food"]
    rules = [
        Rule(SgmlLinkExtractor(allow=('(/section/agriculture-food/news/)((?!:).)*$'),), callback="parse_item", follow=True)
    ]

    def parse_item(self, response):
        item = EuractivNewsItem()
        title = response.xpath('//title/text()')[0].extract()
        article = response.xpath('//p/text()').extract()
        print("Title is: "+title)
        item['title'] = title
        print("Article is: "+",".join(article))
        item['article'] = article
        item['link'] = response.url
        return item
