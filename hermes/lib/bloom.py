# -*- coding: utf-8 -*-

from pybloom import BloomFilter

CAPACITY = 1024 * 1024 * 1024
ERROR_RATE = 0.00001


class MBloomFilter(object):
    """
    The BloomFilter class is suitable to filter request when crawling process
    """

    def __init__(self):
        self.bf = BloomFilter(CAPACITY, ERROR_RATE)

    def __contains__(self, key):
        return key in self.bf


if __name__ == '__main__':
    mbf = MBloomFilter()
