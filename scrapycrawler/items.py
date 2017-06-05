# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class NewsItem(scrapy.Item):
    title = scrapy.Field()
    summary = scrapy.Field()
    body = scrapy.Field()
    url = scrapy.Field()

