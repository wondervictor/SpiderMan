# -*- coding: utf-8 -*-

from Tkinter import *
import tkMessageBox
from threading import Thread
from parser import parser as htmlparse
from crawler import gethtml
from worker import Worker, WorkerConfig
from simple_crawler import SpiderApplication

AUTH_KEY = 'abc'


class LoginView(Frame):

    def __init__(self, app, master=None,):
        Frame.__init__(self, master, width=300, height=200)
        self.app = app
        self.pack()

        self.center_view = Frame(self, width=100, height=100)
        self.left_frame = Frame(self, width=130, height=100)
        self.right_frame = Frame(self, width=140, height=100)

        self.server_label = Label(self.left_frame, text="服务器:",)
        self.port = Label(self.left_frame, text="端口:",)
        self.server_entry = Entry(self.right_frame, width=14)

        self.port_entry = Entry(self.right_frame, width=14)
        self.distribute_button = Button(self.center_view, text="分布式", command=self.distribute, height=2, width=13)
        self.single_button = Button(self.center_view, text="单机", command=self.single, height=2, width=13)
        self.left_frame.propagate(0)
        self.right_frame.propagate(0)
        self.left_frame.grid(padx=2, pady=2, row=0, column=0)
        self.right_frame.grid(padx=0, pady=2,row=0, column=1)
        self.center_view.grid(padx=50, row=1, columnspan=2)
        self.server_label.grid(row=0)
        self.server_entry.grid(row=0)
        self.port.grid(row=1, pady=7)
        self.port_entry.grid(row=1, pady=7)
        self.distribute_button.grid(row=0, pady=4)
        self.single_button.grid(row=1, pady=0)

    def distribute(self):
        if not isinstance(self.app, Application):
            exit(-1)
        server_ip = self.server_entry.get()
        port = self.port_entry.get()
        self.app.login(True, server_ip, port)

    def single(self):
        self.app.login(False)


class MainView(Frame):

    def __init__(self, app, master=None):
        Frame.__init__(self, master, width=600, height=400, bg='gray')
        self.main_frame = Frame(width=600, height=400, bg='gray')
        self.main_frame.pack()
        self.app = app

        self.left_center = Frame(width=300, height=300, bg='white')

        self.right_center = Frame(width=300, height=200, bg='white')
        self.right_down = Frame(width=300, height=100, bg='white')

    def update_info(self, info):
        """
        info: {user:n, question:m, topic:q, answers:p}
        :param info:
        :return:
        """

        


def crawl_func(s):
    return gethtml.get_html(s)


def parse_func(content_type, content):

    return htmlparse.parse_html(content_type, content)


class Logger(object):
    def warn(self, message):
        pass

    def info(self, message):
        pass

    def info(self, message):
        pass

class Application(object):

    def __init__(self):
        self.root = Tk()
        self.root.wm_attributes('-topmost', 1)
        self.current_view = None
        self.worker = None
        self.logger = Logger()
        self.worker_thread = None

    def _resize_window(self, width, height):
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(size)

    def start(self):

        self.current_view = LoginView(self, self.root)
        self._resize_window(300, 200)
        self.root.mainloop()

    def update_func(self, content_type):
        pass

    def login(self, is_distributed, ip="", port=0):

        if is_distributed:
            config = WorkerConfig(
                name='worker',
                task_batchsize=2,
                crawler_threads=8,
                parser_threads=2,
                authkey=AUTH_KEY,
                address=(ip, port)
            )
            self.worker = Worker(
                config=config,
                crawler_func=crawl_func,
                parser_func=parse_func,
                logger=self.logger,
                update_callback=self.update_func
            )
        else:

            self.worker = SpiderApplication(
                parser=parse_func,
                cralwer=crawl_func,
                logger=self.logger,
                update_callback=self.update_func
            )

        self.current_view.destroy()
        self._resize_window(600, 400)
        self.current_view = MainView(self)
        self.worker_thread = Thread(target=self.worker.run)
        self.worker_thread.start()


if __name__ == '__main__':

    app = Application()
    app.start()

