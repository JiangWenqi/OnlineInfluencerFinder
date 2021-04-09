# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from time import time

from itemadapter import ItemAdapter

from OnlineInfluencerFinder.items import OnlineInfluencer


class OnlineInfluencerFinderPipeline:
    def process_item(self, item, spider):
        influencer = OnlineInfluencer()
        influencer['created_time'] = time()
        influencer['updated_time'] = time()
        for (key, value) in item.items():
            influencer[key] = value
        if spider.name == 'twitter':
            influencer['platform'] = 'TWITTER'
        print(influencer)
        return influencer
