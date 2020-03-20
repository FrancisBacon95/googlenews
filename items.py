# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GNItem(scrapy.Item):
    query=scrapy.Field()
    title=scrapy.Field()
    url=scrapy.Field()
    publisher=scrapy.Field()
    content=scrapy.Field()
    date=scrapy.Field()
    est_date=scrapy.Field()
