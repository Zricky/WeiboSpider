# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaWeiboSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    table_name = 'weibo_account'
    id = scrapy.Field()
    info= scrapy.Field()
    flags = scrapy.Field()
