# -*- coding: utf-8 -*-

import multiprocessing
import Queue
from multiprocessing.managers import BaseManager
import smthread


class Master(object):

    def __init__(self, address, authkey):
        """

        :param address: (ip, port)
        :param authkey:
        """
        self.task_queue = Queue.Queue()
        self.link_queue = Queue.Queue()
        self._init_environment()
        self.manager = BaseManager(address=address, authkey=authkey)
        self.tasks = None
        self.links = None

    def _init_environment(self):
        BaseManager.register('get_task_queue', callable=lambda: self.task_queue)
        BaseManager.register('get_link_queue', callable=lambda: self.link_queue)

    def start(self):
        self.manager.start()
        self.tasks = self.manager.get_task_queue()
        self.links = self.manager.get_link_queue()


class Worker(object):

    def __init__(self, config, crawler, parser):
        """
        :param config: task_batchsize, address, authkey, crawler_threads, parser_threads, name
        :param crawler: crawler function
        :param parser: parser function
        """
        self.task_queue = Queue.Queue()
        self.link_queue = Queue.Queue()
        self._init_environment()
        self._manager = BaseManager(address=config.address, authkey=config.authkey)
        self.tasks = None
        self.links = None
        self._content_queue = Queue.Queue()
        self._crawler = crawler
        self._parser = parser
        self._start()
        self._crawler_threads = config.crawler_threads
        self._parser_threads = config.parser_threads
        self._name = config.name

    def _init_environment(self):
        BaseManager.register('get_task_queue', callable=lambda: self.task_queue)
        BaseManager.register('get_link_queue', callable=lambda: self.link_queue)

    def _crawl(self, args):
        content = self._crawler(args)
        self._content_queue.put(content)

    def _handle_content(self, content):

        # do something here
        pass

    def _parse(self, args):

        links, content = self._parser(args)
        self.link_queue.put(links)
        self._handle_content(content)

    def _init_threads(self):

        self.crawler_manager = smthread.SMThreadManager(max_threads=self._crawler_threads, func=self._crawl)
        self.parser_manager = smthread.SMThreadManager(max_threads=self._parser_threads, func=self._parse)

    def _start(self):
        self._manager.connect()
        self.tasks = self._manager.get_task_queue()
        self.links = self._manager.get_link_queue()

    def run(self):

        while True:
            try:
                url = self.tasks.get(timeout=2)
                self.crawler_manager.do(url)
            except Queue.Empty:
                print("URL queue is empty now ....")

            try:
                content = self._content_queue.get(timeout=2)
                self.parser_manager.do(content)

            except Queue.Empty:
                print("Worker content queue is empty now ...")














