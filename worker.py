# -*- coding: utf-8 -*-

import Queue
import argparse
import collections
import multiprocessing
from multiprocessing.managers import BaseManager

from common import log
from store import store
from utils import url_check
from parallel import smthread
from crawler import login, gethtml
from parser import parser as htmlparse


WorkerConfig = collections.namedtuple("WorkerConfig",
                                      "task_batchsize, address, authkey, crawler_threads, parser_threads, name")

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


class Worker(object):

    def __init__(self, config, crawler_func, parser_func, logger=None, update_callback=None):

        # log
        if logger is None:
            self.logger = log.Logger('Worker')
        self.update_callback = update_callback
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
        if content is not None:
            self.parser_manager.do((url, content))
            self.logger.info("[Crawler] Finish crawling %s" % url)
        else:
            self.crawler_manager.do(url)
            self.logger.error("[Crawler] Crawler Failed %s" % url)

    def _handle_content(self, content, content_type):
        """
        处理解析出来的content
        :param content:
        :return:
        """
        store.save_file(content_type, content)
        self.update_callback(content_type)

    def _parse(self, args):
        """
        Parser线程解析函数，解析出content和url
        :param args:
        :return:
        """
        url, content = args
        content_type = url_check.get_url_type(url)
        content_type, links, content = self._parser_func(content_type, content)
        if len(links):
            try:
                self.links.put(links)
            except Exception as e:
                self.logger.error('[Parser] Put url exception %s' % e.message)
        self.logger.info("[Parser] Finish parsing %s" % url)
        self._handle_content(content, content_type)

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
                self.crawler_manager.do(url)
            except Queue.Empty:
                self.logger.info('URL Queue is Empty now ...')
                print("URL queue is empty now ....")

            try:
                url_, content = self._content_queue.get(timeout=1)
                self.parser_manager.do((url_, content))

            except Queue.Empty:
                self.logger.info('Worker Content is Empty now ...')


# Test Distributed

def crawl_func(s):
    return gethtml.get_html(s)


def parse_func(content_type, content):

    return htmlparse.parse_html(content_type, content)


def test_master():

    master = Master(('0.0.0.0', 23333), AUTH_KEY)
    urls = [
        'https://www.zhihu.com/question/26006703',
        'https://www.zhihu.com/topic',
        'https://www.zhihu.com/topic/19565870',
        'https://www.zhihu.com/topic/19550355',
        'https://www.zhihu.com/question/264580669',
        'https://www.zhihu.com/people/webto/',
        'https://www.zhihu.com/question/29130226/answer/284394337',
        'https://www.zhihu.com/question/30943322',
        'https://www.zhihu.com/question/52253320/answer/284550438',
    ]
    master.start(urls)
    master.run()


def test_worker(ip):

    config = WorkerConfig(
        name='worker',
        task_batchsize=2,
        crawler_threads=8,
        parser_threads=2,
        authkey=AUTH_KEY,
        address=(ip, 23333)
    )

    worker = Worker(config=config, crawler_func=crawl_func, parser_func=parse_func)

    worker.run()


# if __name__ == '__main__':
#     multiprocessing.current_process().authkey = AUTH_KEY
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--worker', type=int, default=1, help='worker node')
#     parser.add_argument('--master_ip', type=str, default='0.0.0.0', help='Master IP')
#
#     args = parser.parse_args()
#
#     if args.worker == 1:
#         test_worker(args.master_ip)
#     else:
#         test_master()


