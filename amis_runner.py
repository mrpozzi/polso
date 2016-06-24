from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

spiders = ['bloomberg', 'noggers', 'worldgrain', 'euractiv', 'agrimoney']

for spider in spiders:
    process.crawl(spider)
process.start()

