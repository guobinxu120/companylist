# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy import Request
from urlparse import urlparse
from json import loads
from datetime import date
# import json
import re, csv
from collections import OrderedDict

class companylistSpider(scrapy.Spider):

    name = "companylist_spider"

    use_selenium = False

    next_count = 1
###########################################################

    def __init__(self, categories=None, *args, **kwargs):
        super(companylistSpider, self).__init__(*args, **kwargs)

        if not categories:
            raise CloseSpider('Received no categories!')
        else:
            self.categories = categories

        f1 = open(categories)
        csv_items = csv.DictReader(f1)
        self.start_urls = []
        for i, row in enumerate(csv_items):
            self.start_urls.append(row)
        f1.close()
        # self.start_urls = loads(self.categories).keys()

###########################################################

    def start_requests(self):
        for category in self.start_urls:
            yield Request(('https://companylist.org')+category['Page'], callback=self.parse, meta={'CatURL':category})

###########################################################

    def parse(self, response):
        companies = response.xpath('//*[@class="result-txt"]')
        for company_tag in companies:
            item = OrderedDict()
            item['Company Name'] = company_tag.xpath('./span[@class="result-name"]/a/text()').extract_first()
            item['Url'] = company_tag.xpath('./span[@class="result-name"]/a/@href').extract_first()
            for i in range(1, 6):
                item['Category' + str(i)] = ''

            cats = company_tag.xpath('./span[@class="result-cats"]/a/text()').extract()
            for i, val in enumerate(cats):
                item['Category' + str(i+1)] = val


            yield item


        next = response.xpath('//*[@class="paginator-next "]/@href').extract_first()
        if next:
            yield Request(response.urljoin(next), callback=self.parse, meta=response.meta)
