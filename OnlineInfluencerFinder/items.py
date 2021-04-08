# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UerInfo(scrapy.Item):
    # define the fields for your item here like:
    platform = scrapy.Field()
    tag = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    following_count = scrapy.Field()
    followers_count = scrapy.Field()



