import json
import logging
import re
from urllib.parse import quote

import scrapy

from OnlineInfluencerFinder.items import UerInfo


class TwitterCrawlerSpider(scrapy.Spider):
    name = 'twitter_crawler'
    allowed_domains = ['twitter.com']
    platform = 'twitter'
    tag = 'Tesla'
    url_prefix = (
        'https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1'
        '&include_blocking=1'
        '&include_blocked_by=1'
        '&include_followed_by=1'
        '&include_want_retweets=1'
        '&include_mute_edge=1'
        '&include_can_dm=1'
        '&include_can_media_tag=1'
        '&skip_status=1'
        '&cards_platform=Web-12'
        '&include_cards=1'
        '&include_ext_alt_text=true'
        '&include_quote_count=true'
        '&include_reply_count=1'
        '&tweet_mode=extended'
        '&include_entities=true'
        '&include_user_entities=true'
        '&include_ext_media_color=true'
        '&include_ext_media_availability=true'
        '&send_error_codes=true'
        '&simple_quoted_tweet=true'
        '&count=20'
        '&query_source=typed_query'
        '&pc=1'
        '&spelling_corrections=1'
        '&ext=mediaStats%2ChighlightedLabel'
    )

    # 1. copy cookies from your browser
    cookies_string = 'personalization_id="v1_x2BJaWSUFvXK0r3tVQz7/Q=="; guest_id=v1:158980287506687036; _ga=GA1.2.1462373164.1589802879; kdt=4wjvCXbNMpEllrizcFCLFoJ4D6Elg2SPWekey9Tv; remember_checked_on=1; csrf_same_site_set=1; rweb_optin=side_no_out; csrf_same_site=1; auth_token=55fefe491cb1d88611c3c029fb5f0d3e65216733; twid=u=4307766559; ct0=a871a2bdd27b50564468aaa19d94ad03981b1d24245184ae21d66fe8c189c7bc13c098814a9bbe4c229dc01a32bd5498a2ec9e3d9d4108d4621aa8002f6d30bb144c46e9876242e18c97467dc94d2886; ads_prefs="HBERAAA="; eu_cn=1; night_mode=0; external_referer=padhuUp37zj9xuUOXCNFvGXUXmFWu3h9RbvCou2th62t8qpRtR3BhPixmmJ9DJd0|0|8e8t2xd8A2w='
    cookies = {i.split("=")[0]: i.split("=")[1] for i in cookies_string.split("; ")}

    # 2. overwrite settings.py
    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs=1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
            'x-csrf-token': 'a871a2bdd27b50564468aaa19d94ad03981b1d24245184ae21d66fe8c189c7bc13c098814a9bbe4c229dc01a32bd5498a2ec9e3d9d4108d4621aa8002f6d30bb144c46e9876242e18c97467dc94d2886'
        },
        'CONCURRENT_REQUESTS': 5,
        'DOWNLOAD_DELAY': 2
    }

    def start_requests(self, cursor=None):

        if cursor:
            url = self.url_prefix + '&q={query}' + '&cursor={cursor}'
            # Fill in the query content
            url = url.format(query=quote(self.tag), cursor=quote(cursor))
        else:
            url = self.url_prefix + '&q={query}'
            url = url.format(query=quote(self.tag))
        print(url)

        yield scrapy.Request(
            url,
            callback=self.parse,
            cookies=self.cookies
        )

    def parse(self, response):
        users = json.loads(response.body)['globalObjects']['users']
        for user in users.values():
            user_info = UerInfo()
            user_info['platform'] = self.platform
            user_info['tag'] = self.tag
            user_info['id'] = user['screen_name']
            user_info['name'] = user['name']
            user_info['following_count'] = user['friends_count']
            user_info['followers_count'] = user['followers_count']
            yield user_info
        # go to next page
        cursor = re.compile('"(scroll:[^"]*)"').search(response.text).group(1)
        for r in self.start_requests(cursor=cursor):
            yield r
