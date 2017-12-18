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
        self._init_environment()
        self.manager = BaseManager(address=address, authkey=authkey)
        self.tasks = None

    def _init_environment(self):
        BaseManager.register('get_task_queue', callable=lambda: self.task_queue)

    def start(self):
        self.manager.start()
        self.tasks = self.manager.get_task_queue()


class Worker(object):

    def __init__(self, task_batchsize, address, authkey):
        """

        :param task_batchsize:
        :param address:
        :param authkey:
        """
        self.task_queue = Queue.Queue()
        self._init_environment()
        self.manager = BaseManager(address=address, authkey=authkey)
        self.tasks = None
        self.content_queue = Queue.Queue()

    def _init_environment(self):
        BaseManager.register('get_task_queue', callable=lambda: self.task_queue)

    def start(self):
        self.manager.connect()
        self.tasks = self.manager.get_task_queue()

    def run(self, func):
        pass






