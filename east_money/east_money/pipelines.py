# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import pymongo


class EastMoneyPipeline:
    client = None
    db = None

    def open_spider(self, spider):
        print('----开始爬虫----')
        self.client = pymongo.MongoClient(host=spider.settings['HOST'], port=int(spider.settings['PORT']))
        self.db = self.client[spider.settings['SQL']]

    def close_spider(self, spider):
        self.client.close()
        print('----结束爬虫----')


    def process_item(self, item, spider):
        self.db[spider.settings['SET']].insert_one(dict(item))
