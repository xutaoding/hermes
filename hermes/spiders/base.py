# -*- coding: utf-8 -*-

from redis import StrictRedis

from hermes.utils.exceptions import (
    MetaError
)
from ..lib.mongo import MongoClient
from ..settings import config


class ScrapyMetaClass(type):
    def __new__(mcs, class_name, bases, namespace):
        if hasattr(namespace, 'redis'):
            raise MetaError("Create Spider class don't exist redis attribute.")

        namespace['redis'] = StrictRedis(**config.REDIS_CONFIG)
        namespace['start_urls_key'] = config.START_URLS_KEY
        namespace['start_urls_db'] = MongoClient(**config.MONGO_CONF['scrapy_start_urls'])

        mongo_conf_db = MongoClient(**config.MONGO_CONF['scrapy_conf'])
        spider_class = super(ScrapyMetaClass, mcs).__new__(mcs, class_name, bases, namespace)
        spider_class.mongo_conf_db = mongo_conf_db

        return spider_class


