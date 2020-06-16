# -*- coding: utf-8 -*-

import jmespath
import pickle
import pymongo
import re

from os import path
from scrapy import signals


class RealestatePipeline(object):
    def __init__(self, settings):
        expr = settings.get('JMESPATH')
        self.jmes = jmespath.compile(expr) if expr else None
        self.item_keys = set()
        self.item_keys_filename = 'item_keys.pickle'

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.settings)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        return o

    def process_item(self, item, spider):
        scraped = spider.crawler.stats.get_value('scraped_pages')
        total = spider.crawler.stats.get_value('selected_pages')

        titulo = item.get('TituloPagina')
        if titulo:
            item['TituloPagina'] = re.sub('(?i)\s*-\s*zap\s*im[óo]veis\s*',
                                          '', titulo)

        spider.logger.info('Pages: [{}/{}] - {:.0%}'.format(
            scraped, total, scraped/total))
        spider.logger.info('Item[{}]: {}'.format(
            spider.crawler.stats.get_value('item_scraped_count') or 0,
            item.get('TituloPagina')))

        self.item_keys.update(k for k, v in item.items()
                if v and not isinstance(v, bool))

        return self.jmes.search(item) if self.jmes else item

    def spider_opened(self, spider):
        if path.isfile(self.item_keys_filename):
            with open(self.item_keys_filename, 'rb') as f:
                self.item_keys.update(pickle.load(f))

    def spider_closed(self, spider):
        if self.item_keys:
            with open(self.item_keys_filename, 'wb') as f:
                pickle.dump(self.item_keys, f)
            with open('jmespath.txt', 'w') as f:
                f.write('{\n')
                f.writelines('  {0}:{0}\n'.format(k) for k in self.item_keys)
                f.write('}')

class MongoDBPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        # TODO [romeira]: update if same id {25/04/17 20:14}
        self.collection.insert(item)
        return item
