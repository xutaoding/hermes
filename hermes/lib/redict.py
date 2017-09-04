# -*- coding: utf-8 -*-

import json

import redis
import six

from hermes.utils.exceptions import MetaError
from ..settings import config


class RedisMetaClass(type):
    def __new__(mcs, class_name, bases, namespace):
        if hasattr(namespace, 'redis'):
            raise MetaError("Create class don't exist redis attribute.")

        namespace['settings_key'] = config.SETTINGS_KEY
        namespace['start_urls_key'] = config.START_URLS_KEY
        namespace['redis'] = redis.StrictRedis(**config.SPIDER_REDIS_CONFIG)
        return super(RedisMetaClass, mcs).__new__(mcs, class_name, bases, namespace)


class ReDictBase(dict):
    """ Using Redis hash mapping """

    def __init__(self, key):
        self.key = key
        r_data = self.redis.hgetall(self.key)
        data = json.loads(r_data.decode('utf-8'))

        super(Base, self).__init__(**data)

    def __getitem__(self, name):
        value = dict.__getitem__(self, name)
        _value = self.redis.hget(self.key, name)

        try:
            r_value = json.loads(_value.decode('utf-8'))
        except ValueError:
            r_value = json.load(_value)

    def __setitem__(self, name, value):
        pass

    def __delitem__(self, name):
        pass

    def is_equal(self, obj1, obj2):
        if isinstance(obj1, str):
            pass


class WizardSettings(six.with_metaclass(RedisMetaClass, ReDictBase)):
    """ Every spider task settings store to redis """


class CrawlerTask(six.with_metaclass(RedisMetaClass, ReDictBase)):
    """ Required all configs and extraction rule to tasks of spider """


if __name__ == '__main__':
    pass


