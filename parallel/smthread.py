# -*- coding: utf-8 -*-

import threading
import Queue
from time import sleep


class SMThread(threading.Thread):

    def __init__(self,func=None, args=None, name="", callback=None):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args
        self.callback = callback

    def update(self, func, args, name, callback):
        self.name = name
        self.func = func
        self.args = args
        self.callback = callback

    def run(self):
        print('run in thread: %s' % self.name)
        self.func(self.args)
        self.callback(self)

    def update_task(self, func, args):
        self.func = func
        self.args = args

    def __str__(self):
        return "<Thread Name: %s >" % self.name


class SMThreadManager(object):

    def __init__(self, max_threads=8):
        """
        Init SMThreadManager
        :param max_threads: 最大线程数
        """
        self.max_threads = max_threads
        self.threads = []
        self.task_queue = Queue.Queue()
        self.deamon_thread = threading.Thread()

    def start_thread(self, func, args, name=None, daemon=True):
        """
        新建线程
        :param func: 函数 def func(args)
        :param args: 函数参数
        :param name: 线程名
        :param daemon: 守护进程
        :return:
        """
        def thread_callback(thread_obj):
            print(thread_obj)
            print(self.task_queue.qsize())
            if not thread_obj.is_alive() and not self.task_queue.empty():
                func, args, _ = self.task_queue.get()
                thread_obj.update_task(func, args)
                thread_obj.run()

        thread_id = self._get_free_thread()
        if thread_id != -1:
            if name is None:
                name = '<SMThread-%s>' % thread_id
            self.threads[thread_id].daemon = daemon
            self.threads[thread_id].update(func, args, name, thread_callback)
            self.threads[thread_id].run()
        else:
            self.task_queue.put((func, args, daemon))
        return thread_id

    def _get_free_thread(self):
        """
        获得空闲进程
        :return:
        """
        if len(self.threads) < self.max_threads:
            new_thread = SMThread()
            self.threads.append(new_thread)
            thread_id = len(self.threads)-1
            return thread_id
        else:
            for i in xrange(self.max_threads):
                if not self.threads[i].is_alive():
                    return i
            return -1

    def run_thread(self, idx):
        if idx >= len(self.threads):
            return
        self.threads[idx].run()


def test_thread_manager():

    smt_manager = SMThreadManager()

    names = ['name_%s_%s' % (x, x) for x in range(100)]

    def func(name):
        print('hello %s' % name)
        sleep(2)

    for i in range(100):
        smt_manager.start_thread(func, names[i])

test_thread_manager()


