# -*- coding: utf-8 -*-

import six
from copy import deepcopy

import scrapy

from .base import RedisMetaClass
from ..utils.extractor_conf import ExtractorConf


class WizardSpider(six.with_metaclass(RedisMetaClass, scrapy.Spider)):
    name = 'wizard'
    throttle_count = 1000

    def __init__(self, *args, **kwargs):
        """ The class general suit to crawl static or dynamic html, even json response """
        self.job_idf = self.settings['job_idf']
        self.spider_conf = self.mongo_conf_db.get({'_id': self.job_idf})

        if self.spider_conf is None:
            self.spider_conf = kwargs.pop('spider_conf', {})

        super(WizardSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        """ Obtain args from commandline argument or from DB to launch spider """
        # start_urls_key = self.start_urls_key.format(self.job_idf)
        elements_conf = self.spider_conf.pop('elements_conf', {})
        request_conf = self.spider_conf.pop('request_conf', {})
        cookies_str = request_conf.pop('Cookie', '') or request_conf.pop('cookie', '')
        cookies = cookies_str and dict([s.split('=', 1) for s in cookies_str.split(';')]) or {}

        url = elements_conf.pop('starter_url')
        meta = {'spider_conf': self.spider_conf}

        if url:
            yield scrapy.Request(url, meta=meta, headers=request_conf, cookies=cookies)

    @classmethod
    def update_settings(cls, settings):
        """ Before initializing Spider Class, configure `job_idf` to spider settings """
        job_idf = settings['job_idf']
        spider_conf = cls.mongo_conf_db.get({'_id': job_idf})
        scry_settings = ExtractorConf(spider_conf).scrapy_settings

        custom_settings = cls.custom_settings or {}
        custom_settings.update(scry_settings)
        settings.setdict(custom_settings, priority='spider')

    def parse(self, response):
        spider_conf = response.meta['spider_conf']
        goto_next = spider_conf.pop('goto_next')
        goto_url_css = spider_conf.pop('togo_urls')
        pagination = spider_conf.pop('pagination')

        if goto_url_css:
            for next_url in response.css(goto_url_css):
                url = response.urljoin(next_url)

                yield scrapy.Request(
                    url=url, meta={},
                    headers=response.request.headers, cookies=response.request.cookies,
                    callback=''''''''
                )
        # for elem_or_field, css_prth in spider_conf.iteritems():


    @staticmethod
    def close(spider, reason):
        spider.mongo_conf_db.close()

        closed = getattr(spider, 'closed', None)
        if callable(closed):
            return closed(reason)


