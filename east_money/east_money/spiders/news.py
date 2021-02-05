import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import pymongo
from east_money.items import EastMoneyItem


class NewsSpider(CrawlSpider):
    name = 'news'
    start_urls = ['http://global.eastmoney.com/a/cqqdd.html']


    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@id="pagerNoDiv"]'), follow=True),  # 所有页
        Rule(LinkExtractor(allow=r'eastmoney.com/a/\d*.html', restrict_xpaths='//ul[@id="newsListContent"]'),  # 当前页面的链接
             callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        item = EastMoneyItem()
        item['title'] = response.xpath('//div[@class="newsContent"]/h1/text()').extract_first()
        item['article'] = response.xpath('//div[@id="ContentBody"]').xpath('string(.)').extract_first().replace(' ', '').replace('\r', '').replace('\n', '')
        yield item
