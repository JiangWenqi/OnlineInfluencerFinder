import json
import logging
import re
from urllib.parse import quote

import scrapy

from OnlineInfluencerFinder.items import TwitterUser


class TwitterCrawlerSpider(scrapy.Spider):
    name = 'twitter'
    allowed_domains = ['twitter.com']
    tag = 'Tesla'
    url = (
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
        f'&q={quote(tag)}'
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
        'DOWNLOAD_DELAY': 10  # per request waiting seconds
    }

    # default beginning method when start this spider
    def start_requests(self):
        yield scrapy.Request(
            self.url,
            callback=self.parse,
            cookies=self.cookies
        )

    # the main method to extract content
    def parse(self, response):
        users = json.loads(response.body)['globalObjects']['users']
        for user in users.values():
            twitter_user = TwitterUser()
            twitter_user['tag'] = self.tag
            twitter_user['id'] = user['screen_name']
            twitter_user['name'] = user['name']
            twitter_user['following_count'] = user['friends_count']
            twitter_user['followers_count'] = user['followers_count']
            yield twitter_user
        # go to next page
        cursor = re.compile("(scroll:[^\"]*)").search(response.text).group(1)
        # Fill in the query content
        if cursor:
            next_url = self.url + f'&cursor={quote(cursor)}'
            yield scrapy.Request(
                next_url,
                callback=self.parse,
                cookies=self.cookies
            )
