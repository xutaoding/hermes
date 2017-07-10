# -*- coding: utf-8 -*-

import six

import scrapy
from redis import StrictRedis

from hermes.exceptions import (
    MetaError
)
from hermes.settings import config


class RedisMetaClass(type):
    def __new__(mcs, class_name, bases, namespace):
        if hasattr(namespace, 'redis'):
            raise MetaError("Create Spider class don't exist redis attibute.")

        namespace['redis'] = StrictRedis(**config.SPIDER_REDIS_CONFIG)
        namespace['start_urls_prefix_key'] = config.REDIS_START_URLS_PREFIX_KEY
        return super(RedisMetaClass, mcs).__new__(mcs, class_name, bases, namespace)


class WizardSpider(six.with_metaclass(RedisMetaClass, scrapy.Spider)):
    name = 'wizard'
    throttle_count = 1000

    def __init__(self, *args, **kwargs):
        """ The class general suit to crawl static or dynamic html, even json response """
        self.spider_idf = kwargs.pop('spider_idf')

        if self.spider_idf is None:
            raise ValueError('Launch spider must have a unique identifier keyword.')

        super(WizardSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        start_urls_key = self.start_urls_prefix_key.format(self.spider_idf)

    def parse(self, response):
        pass


if __name__ == '__main__':
    w = WizardSpider()

