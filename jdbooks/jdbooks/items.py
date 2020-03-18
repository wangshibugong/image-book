# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdbooksItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    first_title=scrapy.Field()
    second_title=scrapy.Field()
    second_url=scrapy.Field()
    book_name=scrapy.Field()
    book_price=scrapy.Field()
    book_url=scrapy.Field()
    image_url=scrapy.Field()
