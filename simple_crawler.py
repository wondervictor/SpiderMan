# -*- coding:utf-8 -*-

"""
Simple Crawler

单机版

"""

from common import log
from parser import parser
from crawler import gethtml
from crawler import login
from parallel import smthread


class Application(object):

    def __init__(self):
        self.logger = log.Logger('Application')
        self.crawler_manager = smthread.SMThreadManager(max_threads=4, func=self._crawl)
        self.parser_manager = smthread.SMThreadManager(max_threads=2, func=self._parse)
        self.login = login.Login()

    def start(self):
        self.login.check()

    def _parse(self, content):
        """
        解析出内容和url
        :param content:
        :return:
        """
        pass

    def _crawl(self, url):
        """
        Get content
        :param url:
        :return:
        """
        pass

