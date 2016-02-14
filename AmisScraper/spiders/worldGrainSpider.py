from AmisScraper.items import WorldGrainNewsItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule


class WorldGrainSpider(CrawlSpider):
    #log.start(logfile='~/log.txt', loglevel=log.CRITICAL)
    name = "worldgrain"
    allowed_domains = ["world-grain.com"]
    start_urls = ["http://www.world-grain.com"]
    rules = [
        Rule(SgmlLinkExtractor(allow=('(/articles/news_home/)((?!:).)*$'),), callback="parse_item", follow=True)
    ]

    def parse_item(self, response):
        item = WorldGrainNewsItem()
        title = response.xpath('//title/text()')[0].extract()
        article = response.xpath('//p/text()').extract()
        print("Title is: "+title)
        item['title'] = title
        print("Article is: "+",".join(article))
        item['article'] = article
        item['link'] = response.url
        return item
