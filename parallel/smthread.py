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

    def __init__(self, max_threads=8, func=None):
        """
        Init SMThreadManager
        :param max_threads: 最大线程数
        """
        self.max_threads = max_threads
        self.task_queue = Queue.Queue()
        self.threads = []
        self.func = func
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

    def do(self, args):
        """
        重复任务
        :param args: 参数 tuple
        :return:
        """
        assert self.func is not None, "call `do` self.func shouldn't be None, please init it"
        self.task_queue.put((self.func, args))


def __test_thread_manager():

    names = ['name_%s_%s' % (x, x) for x in range(100)]

    def func_(name):
        print('hello %s' % name)
        sleep(2)

    smt_manager = SMThreadManager(func=func_)

    for i in range(100):
        smt_manager.do(names[i])

    sleep(10)


# __test_thread_manager()


