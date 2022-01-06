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

class companylist_itemSpider(scrapy.Spider):

    name = "companylist_item"

    # use_selenium = True

###########################################################

    def __init__(self, categories=None, *args, **kwargs):
        super(companylist_itemSpider, self).__init__(*args, **kwargs)

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
            yield Request(('https://companylist.org')+category['Url'], callback=self.parse, meta={'CatURL':category})

###########################################################

    def parse(self, response):
        item = OrderedDict()
        item['Company Name'] = response.xpath('//*[@class="container"]/h1/text()').extract_first()
        phone_number = response.xpath('//*[@id="phone"]/a/@onclick').extract_first()
        if phone_number:
            item['Phone'] = str(phone_number).replace('phoneClick(this, ', '').replace(')', '')
        else:
            item['Phone'] = ''
        item['Website_url'] = response.url + response.xpath('//*[@id="cdetail-web"]/@href').extract_first()
        item['Address'] = response.xpath('//*[@itemprop="address"]/@content').extract_first().replace('<br />', ' ')
        cats = response.meta['CatURL']
        for i in range(1, 6):
            item['Category' + str(i)] = cats['Category' + str(i)]
        yield item

