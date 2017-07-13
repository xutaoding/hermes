# -*- coding: utf-8 -*-

import re
import six
from copy import deepcopy

import scrapy

from .base import ScrapyMetaClass
from ..utils.extractor_conf import ExtractorConf


class WizardSpider(six.with_metaclass(ScrapyMetaClass, scrapy.Spider)):
    name = 'wizard'
    throttle_count = 1000

    def __init__(self, *args, **kwargs):
        """ The class general suit to crawl static or dynamic html, even json response """
        self.job_idf = self.settings['job_idf']
        self.spider_conf = self.mongo_conf_db.get({'_id': self.job_idf})

        if self.spider_conf is None:
            self.spider_conf = kwargs.pop('spider_conf', {})

        super(WizardSpider, self).__init__(*args, **kwargs)

    @staticmethod
    def get_cookies(cookies_str):
        cookies = []

        for each_cookie in cookies_str.split(';'):
            cookie_kv = each_cookie.strip().split('=', 1)
            if len(cookie_kv) == 2:
                cookies.append(cookie_kv)

        return dict(cookies)

    def start_requests(self):
        """ Obtain args from commandline argument or from DB to launch spider """

        elements_conf = self.spider_conf.pop('elements_conf', {})
        request_conf = self.spider_conf.pop('request_conf', {})

        cookies_str = request_conf.pop('Cookie', '') or request_conf.pop('cookie', '')
        cookies = self.get_cookies(cookies_str=cookies_str)

        starter_urls = elements_conf.pop('starter_urls', [])
        meta = {'elements_conf': elements_conf}

        for url in starter_urls:
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

    @staticmethod
    def get_headers_from_request(response):
        headers = response.request.headers
        cookies = response.request.cookies

        return {'headers': headers, 'cookies': cookies}

    def retry_status200_timeout(self, response, callback):
        request = None

        url = response.url
        max_download_count = response.meta.get('max_download_count', 1)
        timeout_m = re.compile(r'setTimeout', re.S).search(response.body)

        if timeout_m and response.status == 200:
            if max_download_count <= 6:
                response.meta['max_download_count'] = max_download_count + 1

                request = scrapy.Request(
                    url=url, callback=callback, meta=response.meta,
                    dont_filter=True, **self.get_headers_from_request(response)
                )
        return request

    @staticmethod
    def parse_fields(response, element_conf):
        meta_fields = {}
        fields_selector = {}
        deepcopy_conf = deepcopy(element_conf)

        for k, css_list in deepcopy_conf.iteritems():
            if k.split('_', 1)[0] == 'field':
                fields_selector[k] = css_list

        for field, css_list in fields_selector.iteritems():
            for field_css in css_list:
                field_value = ''.join(response.css(field_css).extract())

                if field_value:
                    meta_fields[field] = field_value
                    break

        return meta_fields

    def parse(self, response):
        # `elements_conf` don't include `starter_urls` key
        request = self.retry_status200_timeout(response, callback=self.parse)
        if request is not None:
            yield request
            return

        elements_conf = deepcopy(response.meta['elements_conf'])
        goto_next_conf = elements_conf.pop('goto_next', {})

        if elements_conf.get('pagination'):
            deepcopy_conf = deepcopy(elements_conf)
            page_meta = {'elements_conf': deepcopy_conf}
            page_meta.update(response.meta)

            pagination_list = deepcopy_conf['pagination']

            for pagination_path in pagination_list:
                pagination_url = response.css(pagination_path).extract_first()

                if pagination_url:
                    yield scrapy.Request(
                        url=pagination_url, meta=page_meta,
                        **self.get_headers_from_request(response)
                    )

        if elements_conf.get('goto_urls'):
            elements_conf.pop('pagination', None)
            goto_url_list = elements_conf['goto_urls']

            for goto_url_path in goto_url_list:
                for next_url in response.css(goto_url_path).extract():
                    next_url = (next_url or '').strip()
                    if not next_url:
                        continue

                    url = response.urljoin(next_url)
                    meta = self.parse_fields(response, elements_conf)
                    meta.update(response.meta)
                    meta.update({'elements_conf': goto_next_conf})

                    yield scrapy.Request(
                        url=url, meta=meta,
                        **self.get_headers_from_request(response)
                    )

        if not goto_next_conf:
            yield self.parse_detail(response)

    def parse_detail(self, response):
        def get_fields_result(queryset_with_meta):
            _fields = {}

            for mk, mv in queryset_with_meta.iteritems():
                key = mk.split('_', 1)
                if key[0] == 'field':
                    _fields[key[1]] = mv

            return _fields

        elements_conf = response.meta['elements_conf']
        meta_fields = get_fields_result(response.meta)
        tmp_fields = self.parse_fields(response, elements_conf)

        item = {}
        item.update(meta_fields)
        item.update(tmp_fields)

        return item

    @staticmethod
    def close(spider, reason):
        spider.mongo_conf_db.close()

        closed = getattr(spider, 'closed', None)
        if callable(closed):
            return closed(reason)


