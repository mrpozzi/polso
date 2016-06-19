# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import pymongo
import os
from scrapy.exceptions import DropItem


DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'resources'))


class SanitizeArticlePipeline(object):
    def __init__(self):
        stf = open(DATA_DIR+'/stop_words.txt', 'r')
        stop_words = [line.rstrip('\n') for line in stf]
        self.stop_words = set(stop_words)

    def process_item(self, item, spider):
        if 'article' in dict(item):
            sanitized_article = " ".join([x for x in item['article'] if len(x) > 2 and x not in self.stop_words])
            item['article'] = sanitized_article.encode('ascii', 'ignore')
        if len(item['article']) > 0:
            return item
        else:
            raise DropItem("Missing price in %s" % item)


class AmisJsonPipeline(object):
    def __init__(self):
        self.file = open('amis_articles.json', 'ab')

    def process_item(self, item, spider):
        item_dict = dict(item)
        item_dict['source'] = spider.name
        line = json.dumps(item_dict) + "\n"
        self.file.write(line)
        return item


class AmisMongoPipeline(object):

    collection_name = 'amis_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        item_dict = dict(item)
        self.db[self.collection_name].insert(item_dict)
        return item
