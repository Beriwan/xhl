# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XhlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    roomid = scrapy.Field()
    plat = scrapy.Field()
    ranktype = scrapy.Field()
    ranktime = scrapy.Field()
    detail = scrapy.Field()
    Crawltime = scrapy.Field()
    pass

class otherItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    roomid = scrapy.Field()
    plat = scrapy.Field()
    anchor = scrapy.Field()
    achieve = scrapy.Field()
    rankindex = scrapy.Field()
    Crawltime = scrapy.Field()
    gift = scrapy.Field()
    table = scrapy.Field()
