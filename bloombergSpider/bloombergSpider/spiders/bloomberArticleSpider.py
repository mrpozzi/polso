from scrapy.contrib.spiders import CrawlSpider, Rule
from bloombergSpider.items import BloombergNewsArticleItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy import log

class ArticleSpider(CrawlSpider):
    #log.start(logfile='~/log.txt', loglevel=log.CRITICAL)
    name="article"
    allowed_domains = ["bloomberg.com"]
    #start_urls = ["http://www.bloomberg.com/markets"]
    start_urls = ["http://www.bloomberg.com"]
    rules = [
        Rule(SgmlLinkExtractor(allow=('(/news/articles/)((?!:).)*$'),), callback="parse_item", follow=True)
    ]

    def parse_item(self, response):
        item = BloombergNewsArticleItem()
        title = response.xpath('//title/text()')[0].extract()
        article = response.xpath('//p/text()').extract()
        print("Title is: "+title)
        item['title'] = title
        print("Article is: "+",".join(article))
        item['article'] = article
        item['link'] = response.url
        return item
