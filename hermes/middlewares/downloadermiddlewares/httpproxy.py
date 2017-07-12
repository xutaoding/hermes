# -*- coding: utf-8 -*-

import random

from scrapy import signals
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware

from ...utils.util import fake_proxy


class HermesHttpProxyMiddleware(object):
    # def __init__(self, http_proxy_key=None):
    #     self.http_proxy_key = http_proxy_key

    # @classmethod
    # def from_crawler(cls, crawler):
    #     redis = getattr(crawler.spider, 'redis', None)
    #     proxy_key = crawler.settings['SCRAPY_PROXY_IP_KEY']
    #     http_proxy = redis.lpop(proxy_key) if redis else []
    #
    #     crawler.signals.connect(cls.close, signals.spider_closed)
    #     return cls(http_proxy)

    @classmethod
    def close(cls, spider, reason):
        # Origin thought finished proxy ip, push proxy ip to Queue when `spider` finished,
        # But don't have to do that, operate Queue `rpoplpush` method from redis
        pass

    def process_request(self, request, spider):
        # spider.setting with classmethod from_crawler method crawler.setting is same
        # `SCRAPY_PROXY_IP_KEY` key can get from the `settings` variable

        fake_proxy_list = []

        for _ in range(random.randint(1, 3)):
            fake_proxy_list.append(fake_proxy())

        request.headers['X-Forwarded-For'] = ','.join(fake_proxy_list)

        # redis = getattr(spider, 'redis', None)

        # if redis and self.http_proxy_key:
        #     http_proxy = redis.rpoplpush(self.http_proxy_key, self.http_proxy_key)
        # else:
        #     http_proxy = None

        # http_proxy = '114.239.2.44:808'
        # if http_proxy and 'proxy' not in request.meta:
        #     request.meta['proxy'] = 'https://' + http_proxy
        #
        # print 'dddddd:', request.meta
