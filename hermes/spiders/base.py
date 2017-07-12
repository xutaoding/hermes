# -*- coding: utf-8 -*-

from redis import StrictRedis

from ..lib.mongo import MongoClient
from ..exceptions import (
    MetaError
)
from ..settings import config


class RedisMetaClass(type):
    def __new__(mcs, class_name, bases, namespace):
        if hasattr(namespace, 'redis'):
            raise MetaError("Create Spider class don't exist redis attibute.")

        namespace['redis'] = StrictRedis(**config.REDIS_CONFIG)
        namespace['start_urls_key'] = config.START_URLS_KEY
        namespace['mongo_conf_db'] = MongoClient(**config.MONGO_CONF['conf_table'])

        return super(RedisMetaClass, mcs).__new__(mcs, class_name, bases, namespace)