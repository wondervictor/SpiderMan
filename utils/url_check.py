# -*- coding: utf-8 -*-

"""

URL Check

URL查重处理

@dependencies:

1. mmh
2. bitarray

"""
import re
import math
import random

import mmh3
from bitarray import bitarray


urls = [
    'https://www.zhihu.com/question/26006703',
    'https://www.zhihu.com/roundtable/jiqixuexi',
    'https://www.zhihu.com/question/63883507/answer/227019715',
    'https://www.zhihu.com/people/breaknever/activities',
    'www.baidu.com',
    'https://www.zhiha.com/dqwfq3/',
    'https://www.zhihu.ca/wdqd21f'
]

"""
## URL Type:

* topic
* people
* roundtable
* question

"""

def get_url_type(url):
    """
    https://www.zhihu.com/xxxxx/1231234/xwf3qwrvq
    :param url:
    :return: xxxxxxx
    """
    s = url.replace('//', 'a')
    s = s.split('/')
    if len(s) < 2:
        return None
    return s[1]


def get_url_id(url):

    """
    https://www.zhihu.com/question/xxxxxx/xwf3qwrvq
    :param url:
    :return: xxxxxxx
    """
    s = url.replace('//', 'a')
    s = s.split('/')
    if len(s) < 3:
        return None
    return s[2]


def filter_urls(urls):
    """
    URL 过滤、标签
    过滤规则：知乎之外的网站、

    :param urls:
    :return: [(URL, URL_TYPE, URL_CONTENT)]
    """
    pattern = '(http|https)://www.zhihu.com/.*?'

    def match_(url):
        if re.match(pattern, url, re.S) is None:
            return False
        return True

    urls = filter(match_, urls)

    def get_type(url):

        s = url.replace('//', 'a')
        s = s.split('/')
        url_type = s[1]
        url_content = s[2]
        return url, url_type, url_content

    urls = map(get_type, urls)
    return urls


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


if __name__ == '__main__':

    urls = filter_urls(urls)
    for i in urls:
        print (i)