import scrapy
from urlparse import urlparse
from scrapy import Request
from scrapy.utils.response import open_in_browser
from collections import OrderedDict
class CategoriesOfcompanylist(scrapy.Spider):

	name = "categories_of_companylist"
	start_urls = ('https://companylist.org/categories/',)

	use_selenium = False
	def parse(self, response):

		categories = response.xpath('//*[contains(@class, "level-0")]')
		# categories.extend( response.xpath('//*[contains(@class, "level-1")]'))
		for cat in categories:
			item = OrderedDict()
			item['Category'] = cat.xpath('./a/@title').extract_first()
			item['Page'] = cat.xpath('./a/@href').extract_first()
			yield item

		# links = []
		# # print len(categories)
		# # for cate in categories:
		# # 	if cate.xpath('.//ul'):
		# # 		links = links + cate.xpath('.//ul/li/a/@href').extract()
		# # 	else:
		# # 		links = links + cate.xpath('./a/@href').extract()
        #
		#
		# yield {'links':list(urlparse(x).path for x in categories)}
