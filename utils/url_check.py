# -*- coding: utf-8 -*-

"""

URL Check

URL查重处理

@dependencies:

1. mmh
2. bitarray

"""

from bitarray import bitarray
import math
import mmh3
import random


def check_urls(urls, bloom_filter):

    assert isinstance(bloom_filter, BloomFilter), "Use Bloom Filter"

    def preprocess(x):
        """
        www.zhihu.com/quesiotn/dqwfqg[?w=cw&fqw=]
        :param x:
        :return:
        """
        return x.split('?')[0]

    urls = map(urls, preprocess)
    result = []

    for url in urls:

        if len(url) == 0:
            continue
        if not bloom_filter.check(url):
            result.append(url)
            bloom_filter.add(url)

    return result


class BloomFilter(object):

    def __init__(self, item_count, prob):

        self.prob = prob
        self.size = self.get_size(item_count, prob)
        self.hash_count = self.get_hash_count(self.size, item_count)
        self.bit_array = bitarray(self.size)
        self.bit_array.setall(0)

    @classmethod
    def get_size(self, n, p):
        """

        :param n: numbers of elements in the filter
        :param p: False Positive Prob
        :return:
        """
        m = -(n*math.log(p))/(math.log(2)**2)
        return int(m)

    def check(self, item):
        for i in xrange(self.hash_count):

            digest = mmh3.hash(item, i) % self.size
            if not self.bit_array[digest]:
                return False
        return True

    def add(self, item):

        digests = []
        for i in xrange(self.hash_count):

            digest = mmh3.hash(item, i) % self.size
            digests.append(digest)

            self.bit_array[digest] = True

    @classmethod
    def get_hash_count(self, m, n):
        """
        k = (m/n)*lg(2)
        :param m: bit array size
        :param n: number of elements
        :return:
        """
        k = (m/n)*math.log(2)
        return int(k)

