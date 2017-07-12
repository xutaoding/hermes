# -*- coding: utf-8 -*-

import redis
import pyreBloom

from hermes.settings import config


CAPACITY = 100000000
ERROR_RATE = 0.0001
BF_REDIS_KEY = 'bloomfiter'


class BloomFilter(object):
    """
    The BloomFilter class is suitable to filter request when crawling process
    """

    def __init__(self,
                 key=BF_REDIS_KEY,
                 capacity=CAPACITY,
                 error=ERROR_RATE,
                 host=config.REDIS_CONFIG['host'],
                 port=config.REDIS_CONFIG['port'],
                 password=config.REDIS_CONFIG.get('password', ''),
                 db=config.REDIS_CONFIG['db']
                 ):
        self.bloom = pyreBloom.pyreBloom(
            key=key,
            capacity=capacity,
            error=error,
            host=host,
            port=port,
            password=password,
            db=db
        )

    def __contains__(self, value):
        """ To redis key(`bloomfiter.0`):
        (1): value don't include value-set, then add value to this key;
        (2): if value in, return True
        """
        if value in self.bloom:
            return True

        return self.add(value)

    def delete(self):
        """ Delete value-set of this redis key """
        return self.bloom.delete()

    def keys(self):
        """ Return a list of the keys used in this bloom filter """
        return self.bloom.keys()

    def add(self, value):
        return self.bloom.add(value)


if __name__ == '__main__':
    boom = BloomFilter()
    # print dir(boom.bloom)
    # print boom.bloom.keys()
    # ss = ['ccc']
    print 'abc' in boom.bloom
    print boom.bloom.add(['abc', 'ccc', 'kkk'])
    # print boom.bloom.delete()
    # print boom.bloom.bits
    # print boom.bloom.hashes

