# -*- coding: utf-8 -*-

import Queue
import collections
import multiprocessing
from multiprocessing.managers import BaseManager

from common import log
from utils import url_check

AUTH_KEY = 'abc'


class Master(object):

    def __init__(self, address, authkey):
        """

        :param address: (ip, port)
        :param authkey:
        """
        self.logger = log.Logger('Master')
        self.task_queue = Queue.Queue()
        self.link_queue = Queue.Queue()
        self._init_environment()
        self._init_checker()
        self.manager = BaseManager(address=address, authkey=authkey)
        self.tasks = None
        self.links = None

    def _init_environment(self):
        BaseManager.register('get_task_queue', callable=lambda: self.task_queue)
        BaseManager.register('get_link_queue', callable=lambda: self.link_queue)

    def _init_checker(self):
        self.checker = url_check.BloomFilter(item_count=10000, prob=0.01)

    def start(self, init_urls):
        self.manager.start()
        self.tasks = self.manager.get_task_queue()
        self.links = self.manager.get_link_queue()

        for url in init_urls:
            self.tasks.put(url)
        self.logger.info("Init finished")

    def run(self):
        """
        更新url queue
        :return:
        """
        while True:
            try:
                urls = self.links.get(timeout=2)
                urls = url_check.check_urls(urls, self.checker)
                for url in urls:
                    self.tasks.put(url)
                self.logger.info('GET URLS: %s' % len(urls))
            except Queue.Empty:
                self.logger.info('Waiting for URLS')
                continue


def test_master(url):

    master = Master(('0.0.0.0', 23333), AUTH_KEY)
    urls = [
        url
        # 'https://www.zhihu.com/question/26006703',
        # 'https://www.zhihu.com/topic',
        # 'https://www.zhihu.com/topic/19565870',
        # 'https://www.zhihu.com/topic/19550355',
        # 'https://www.zhihu.com/question/264580669',
        # 'https://www.zhihu.com/people/webto/',
        # 'https://www.zhihu.com/question/29130226/answer/284394337',
        # 'https://www.zhihu.com/question/30943322',
        # 'https://www.zhihu.com/question/52253320/answer/284550438',
    ]
    master.start(urls)
    master.run()


if __name__ == '__main__':
    multiprocessing.current_process().authkey = AUTH_KEY

    print("Master is starting to run ....")
    keyword = raw_input("Please enter a keyword to search:")

    url = 'https://www.zhihu.com/search?type=content&q=%s' % keyword
    print("Your First URL is: %s" % url)
    test_master(url)
