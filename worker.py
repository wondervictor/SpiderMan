# -*- coding: utf-8 -*-

import Queue
import argparse
import collections
import multiprocessing
from multiprocessing.managers import BaseManager

from common import log
from parser import parser
from utils import url_check
from parallel import smthread
from crawler import login, gethtml

WorkerConfig = collections.namedtuple("WorkerConfig",
                                      "task_batchsize, address, authkey, crawler_threads, parser_threads, name")

AUTH_KEY = 'abc'


class Task(object):




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
                # urls = url_check.check_urls(urls, self.checker)
                for url in urls:
                    self.tasks.put(url)
                print("GET URLS: %s" % len(urls))
            except Queue.Empty:
                print("No more URLs")
                continue


class Worker(object):

    def __init__(self, config, crawler_func, parser_func):
        """
        :param config: task_batchsize, address, authkey, crawler_threads, parser_threads, name
        :param crawler: crawler function
        :param parser: parser function
        """
        # log
        self.logger = log.Logger('Worker')

        # self.task_queue = Queue.Queue()
        # self.link_queue = Queue.Queue()
        self._init_environment()
        self.login = login.Login()
        self._manager = BaseManager(address=config.address, authkey=config.authkey)
        self.tasks = None
        self.links = None
        self._content_queue = Queue.Queue()
        self._crawler_func = crawler_func
        self._parser_func = parser_func
        self._start()
        self._crawler_threads = config.crawler_threads
        self._parser_threads = config.parser_threads
        self._name = config.name
        self._init_threads()

    def _init_environment(self):
        BaseManager.register('get_task_queue')
        BaseManager.register('get_link_queue')

    def _crawl(self, url):
        """
        网络爬取函数
        :param url:
        :return:
        """
        content = self._crawler_func(url)
        self._content_queue.put(content)
        print("Crawler: args: %s get: %s" % (url, content))

    def _handle_content(self, content):
        """
        处理解析出来的content
        :param content:
        :return:
        """
        # DEBUG
        print(content)
        # do something here
        pass

    def _parse(self, args):
        """
        Parser线程解析函数，解析出content和url
        :param args:
        :return:
        """
        links, content = self._parser_func(args)
        self.links.put(links)
        print(self.links.qsize())
        self._handle_content(content)

    def _init_threads(self):

        self.crawler_manager = smthread.SMThreadManager(max_threads=self._crawler_threads, func=self._crawl)
        self.parser_manager = smthread.SMThreadManager(max_threads=self._parser_threads, func=self._parse)

    def _start(self):
        multiprocessing.current_process().authkey = AUTH_KEY
        self._manager.connect()
        self.tasks = self._manager.get_task_queue()
        self.links = self._manager.get_link_queue()
        self.logger.info("Worker init")

    def run(self):
        # 检查是否需要登录
        self.login.check()

        while True:
            try:
                url = self.tasks.get(timeout=1)
                self.logger.info('get url: %s' % url)
                self.crawler_manager.do(url)
            except Queue.Empty:
                print("URL queue is empty now ....")

            try:
                content = self._content_queue.get(timeout=1)
                self.parser_manager.do(content)

            except Queue.Empty:
                print("Worker content queue is empty now ...")


# Test Distributed

def crawl_func(s):
    return "%s + content" % s


def parse_func(p):

    return ["%s-%d" % (p, x) for x in range(2)], "content"


def test_master():

    master = Master(('0.0.0.0', 23333), AUTH_KEY)
    master.start(['hello', 'world', 'fwqrgfq', 'wgfq34g2', 'qfwef3qg3q', 'wqf3qgqgqq', 'fqwfgqg'])
    master.run()


def test_worker():

    config = WorkerConfig(
        name='worker',
        task_batchsize=4,
        crawler_threads=2,
        parser_threads=4,
        authkey=AUTH_KEY,
        address=('0.0.0.0', 23333)
    )

    worker = Worker(config=config, crawler_func=crawl_func, parser_func=parse_func)

    worker.run()


# if __name__ == '__main__':
#     multiprocessing.current_process().authkey = AUTH_KEY
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--worker', type=int, default=1, help='worker node')
#
#     args = parser.parse_args()
#
#     if args.worker == 1:
#         test_worker()
#     else:
#         test_master()


