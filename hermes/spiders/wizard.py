# -*- coding: utf-8 -*-

import six

import scrapy

from .base import RedisMetaClass
from ..utils.extractor_conf import ExtractorConf


class WizardSpider(six.with_metaclass(RedisMetaClass, scrapy.Spider)):
    name = 'wizard'
    throttle_count = 1000

    def __init__(self, *args, **kwargs):
        """ The class general suit to crawl static or dynamic html, even json response """
        self.job_idf = kwargs.pop('job_idf', '')
        self.spider_conf = self.mongo_conf_db.get({'_id': self.job_idf})

        if self.spider_conf is None:
            self.spider_conf = kwargs.pop('spider_conf', {})

        super(WizardSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        """ Obtain args from commandline argument or from DB to launch spider """
        start_urls_key = self.start_urls_key.format(self.spider_idf)

    @classmethod
    def update_settings(cls, settings):
        # scry_settings = ExtractorConf()

        settings.setdict(cls.custom_settings or {}, priority='spider')

    def parse(self, response):
        pass

    @staticmethod
    def close(spider, reason):
        spider.mongo_conf_db.close()

        closed = getattr(spider, 'closed', None)
        if callable(closed):
            return closed(reason)


