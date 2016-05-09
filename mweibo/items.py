# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MweiboItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    topic = scrapy.Field()
    category = scrapy.Field()
    desc1 = scrapy.Field()
    desc2 = scrapy.Field()
    time = scrapy.Field()
