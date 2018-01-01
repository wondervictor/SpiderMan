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


class Worker(object):

    def __init__(self, config, crawler_func, parser_func, logger=None, update_callback=None):

        # log
        if logger is None:
            self.logger = log.Logger('Worker')
        else:
            self.logger = logger
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
        if self.update_callback:
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

    def exit_app(self):

        exit(0)

