from AmisScraper.items import *
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

# TODO: move all rules to a single file.
# TODO: find a way to clean all the text.


class BloombergSpider(CrawlSpider):
    name = "bloomberg"
    allowed_domains = ["bloomberg.com"]
    # start_urls = ["http://www.bloomberg.com/markets"]
    start_urls = ["http://www.bloomberg.com"]
    rules = [
        Rule(SgmlLinkExtractor(allow='(/news/articles/)((?!:).)*$'), callback="parse_item", follow=True)
    ]

    def parse_item(self, response):
        item = NewsArticleItem()
        title = response.xpath('//title/text()')[0].extract()
        article = response.xpath('//p/text()').extract()
        self.logger.info("Scraping Title: "+title)
        item['title'] = title
        item['article'] = article
        item['link'] = response.url
        return item


class NoggersBlogSpider(CrawlSpider):
    name = "noggers"
    allowed_domains = ["nogger-noggersblog.blogspot.it"]
    start_urls = ["http://nogger-noggersblog.blogspot.it/"]
    rules = [
        # Rule(SgmlLinkExtractor(allow='(/news/articles/)((?!:).)*$'), callback="parse_item", follow=True)
        Rule(SgmlLinkExtractor(allow='((?!:).)*$'), callback="parse_item", follow=True)
    ]

    def parse_item(self, response):
        item = NewsArticleItem()
        title = response.xpath('//title/text()')[0].extract()
        article = response.xpath('//p/text()').extract()
        self.logger.info("Scraping Title: "+title)
        item['title'] = title
        item['article'] = article
        item['link'] = response.url
        return item


class WorldGrainSpider(CrawlSpider):
    name = "worldgrain"
    allowed_domains = ["world-grain.com"]
    start_urls = ["http://www.world-grain.com"]
    rules = [
        Rule(SgmlLinkExtractor(allow='(/articles/news_home/)((?!:).)*$'), callback="parse_item", follow=True)
    ]

    def parse_item(self, response):
        item = NewsArticleItem()
        title = response.xpath('//title/text()')[0].extract()
        article = response.xpath('//p/text()').extract()
        self.logger.info("Scraping Title: "+title)
        item['title'] = title
        item['article'] = article
        item['link'] = response.url
        return item


class EuractivSpider(CrawlSpider):
    name = "euractiv"
    allowed_domains = ["www.euractiv.com"]
    start_urls = ["http://www.euractiv.com/sections/agriculture-food"]
    rules = [
        Rule(SgmlLinkExtractor(allow='(/section/agriculture-food/news/)((?!:).)*$'), callback="parse_item", follow=True)
    ]

    def parse_item(self, response):
        item = NewsArticleItem()
        title = response.xpath('//title/text()')[0].extract()
        article = response.xpath('//p/text()').extract()
        self.logger.info("Scraping Title: "+title)
        item['title'] = title
        item['article'] = article
        item['link'] = response.url
        return item
