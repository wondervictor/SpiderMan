# -*- coding: utf-8 -*-

import threading
import Queue
from time import sleep


class SMThread(threading.Thread):

    def __init__(self, task_queue):
        super(SMThread, self).__init__()
        self.task_queue = task_queue
        self.daemon = True

    def run(self):

        while True:
            (func, args) = self.task_queue.get()
            func(args)
            self.task_queue.task_done()


class SMThreadManager(object):

    def __init__(self, max_threads=8):
        """
        Init SMThreadManager
        :param max_threads: 最大线程数
        """
        self.max_threads = max_threads
        self.task_queue = Queue.Queue()
        self.threads = []
        self._init_thread_pool()

    def _init_thread_pool(self):

        for i in xrange(self.max_threads):

            thread = SMThread(self.task_queue)
            thread.start()
            self.threads.append(thread)

        print("Thread pool initialized")

    def add_task(self, func, args):
        """
        添加任务
        :param func: 函数名
        :param args: 函数参数 tuple
        """
        self.task_queue.put((func, args))


def __test_thread_manager():

    smt_manager = SMThreadManager()

    names = ['name_%s_%s' % (x, x) for x in range(100)]

    def func(name):
        print('hello %s' % name)
        sleep(2)

    for i in range(100):
        smt_manager.add_task(func, names[i])

    sleep(10)


__test_thread_manager()


