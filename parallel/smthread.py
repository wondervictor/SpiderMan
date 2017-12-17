# -*- coding: utf-8 -*-

import threading
import Queue


class SMThread(threading.Thread):

    def __init__(self, func, callback, args, name):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args

    def run(self):
        self.func(self.args)

    def update_task(self, func, args):
        self.func = func
        self.args = args


class SMThreadManager(object):

    def __init__(self, max_threads):
        self.max_threads = max_threads
        self.threads = []
        self.task_queue = Queue.Queue()

    def start_thread(self, func, args, name, daemon=True):
        thread_id = -1
        if len(self.threads) < self.max_threads:
            new_thread = SMThread(func, args, name)
            new_thread.daemon = daemon
            self.threads.append(new_thread)
            thread_id = len(self.threads)-1
        else:
            self.task_queue.put((func, args, daemon))
        return thread_id

    def run_thread(self, idx):
        if idx >= len(self.threads):
            return
        self.threads[idx].run()


