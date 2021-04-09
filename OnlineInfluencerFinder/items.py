# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TwitterUser(scrapy.Item):
    # define the fields for your item here like:
    tag = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    following_count = scrapy.Field()
    followers_count = scrapy.Field()


class OnlineInfluencer(scrapy.Item):
    # define the fields for your item here like:
    platform = scrapy.Field()
    created_time = scrapy.Field()
    updated_time = scrapy.Field()
    tag = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    following_count = scrapy.Field()
    followers_count = scrapy.Field()
