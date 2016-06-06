from AmisScraper.items import NewsArticleItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from datetime import datetime

# TODO: move all rules to a single file.
# TODO: find a way to clean all the text.
# TODO: add error handling (no silent failure...)


class BloombergSpider(CrawlSpider):
    name = "bloomberg"
    allowed_domains = ["bloomberg.com"]
    # start_urls = ["http://www.bloomberg.com/markets"]
    start_urls = ["http://www.bloomberg.com"]
    rules = [
        Rule(LinkExtractor(allow='(/news/articles/)((?!:).)*$'), callback="parse_item", follow=True)
    ]

    def parse_item(self, response):
        item = NewsArticleItem()
        title = response.xpath('//title/text()')[0].extract()
        article = response.xpath('//p/text()').extract()
        self.logger.info("Scraping Title: "+title)
        item['title'] = title
        item['article'] = article
        item['link'] = response.url
        raw_date = response.url.split("/")[-2]
        date = datetime.strptime(raw_date, '%Y-%m-%d')
        item['date'] = str(date)
        return item


class NoggersBlogSpider(CrawlSpider):
    name = "noggers"
    allowed_domains = ["nogger-noggersblog.blogspot.it"]
    start_urls = ["http://nogger-noggersblog.blogspot.it/"]
    rules = [
        # Rule(LinkExtractor(allow='(/news/articles/)((?!:).)*$'), callback="parse_item", follow=True)
        Rule(LinkExtractor(allow='((?!:).)*$'), callback="parse_item", follow=True)
    ]

    def parse_item(self, response):
        item = NewsArticleItem()
        title = response.xpath('//title/text()')[0].extract()
        article = response.xpath('//p/text()').extract()
        self.logger.info("Scraping Title: "+title)
        item['title'] = title
        item['article'] = article
        item['link'] = response.url
        raw_date = title.split("Nogger's Blog: ")[1]
        date = datetime.strptime(raw_date, '%d-%b-%Y')
        item['date'] = str(date)
        return item


class WorldGrainSpider(CrawlSpider):
    name = "worldgrain"
    allowed_domains = ["world-grain.com"]
    start_urls = ["http://www.world-grain.com"]
    rules = [
        Rule(LinkExtractor(allow='(/articles/news_home/)((?!:).)*$'), callback="parse_item", follow=True)
    ]

    def parse_item(self, response):
        item = NewsArticleItem()
        title = response.xpath('//title/text()')[0].extract()
        article = response.xpath('//p/text()').extract()
        self.logger.info("Scraping Title: "+title)
        item['title'] = title
        item['article'] = article
        item['link'] = response.url
        raw_date = "{0}-{1}".format(response.url.split("/")[-2], response.url.split("/")[-3])
        date = datetime.strptime(raw_date, '%m-%Y')
        item['date'] = str(date)
        return item


class EuractivSpider(CrawlSpider):
    name = "euractiv"
    allowed_domains = ["www.euractiv.com"]
    start_urls = ["http://www.euractiv.com/sections/agriculture-food"]
    rules = [
        Rule(LinkExtractor(allow='(/section/agriculture-food/news/)((?!:).)*$'), callback="parse_item", follow=True)
    ]

    def parse_item(self, response):
        item = NewsArticleItem()
        title = response.xpath('//title/text()')[0].extract()
        article = response.xpath('//p/text()').extract()
        self.logger.info("Scraping Title: "+title)
        item['title'] = title
        item['article'] = article
        item['link'] = response.url
        raw_date = article[2].replace(" ", "").replace("\n", "")
        date = datetime.strptime(raw_date, '%m/%d/%Y')
        item['date'] = str(date)
        return item


class AgriMoneySpider(CrawlSpider):
    name = "agrimoney"
    allowed_domains = ["www.agrimoney.com"]
    start_urls = ["http://www.agrimoney.com"]
    rules = [
        Rule(LinkExtractor(allow='(/news/)((?!:).)*$'), callback="parse_item", follow=True)
    ]

    def parse_item(self, response):
        item = NewsArticleItem()
        title = response.xpath('//title/text()')[0].extract()
        raw_date = response.xpath('//font/text()')[2].extract() + response.xpath('//font/text()')[3].extract()
        article = response.xpath('//td/font/p/text()').extract() + response.xpath('//td/font/p/font/text()').extract()
        self.logger.info("Scraping Title: "+title)
        item['title'] = title.replace('Agrimoney.com | ', '')
        item['article'] = article
        item['link'] = response.url
        date = datetime.strptime(raw_date.split(',')[1], ' %d %b %Y')
        item['date'] = str(date)
        return item
