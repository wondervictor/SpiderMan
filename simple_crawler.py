# -*- coding:utf-8 -*-

"""
Simple Crawler

单机版

"""

from parser import parser
from crawler import gethtml
from thread import smthread


class Application(object):

    def __init__(self):
        self.crawler_manager = smthread.SMThreadManager(max_threads=4)
        self.parser_manager = smthread.SMThreadManager(max_threads=2)



