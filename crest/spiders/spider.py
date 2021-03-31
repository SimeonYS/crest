import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import CrestItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class CrestSpider(scrapy.Spider):
	name = 'crest'
	start_urls = ['https://southcrestbank.com/news/']

	def parse(self, response):
		post_links = response.xpath('//h4/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//p[@class="blog-author"]/text()').get()
		date = re.findall(r'\w+\s\d+\,\s\d+', date)
		title = response.xpath('//h1/text()').get()
		content = response.xpath('//div[@class="article-body"]//text()[not (ancestor::header)]').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=CrestItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
