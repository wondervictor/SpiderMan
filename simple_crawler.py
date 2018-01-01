# -*- coding:utf-8 -*-

"""
Simple Crawler

单机线程版

"""
import Queue

from common import log
from store import store
from parser import parser
from crawler import login
from crawler import gethtml
from utils import url_check
from parallel import smthread


class SpiderApplication(object):

    def __init__(self, parser, cralwer, logger=None, update_callback=None):

        if logger is None:
            self.logger = log.Logger('Application')
        else:
            self.logger = logger
        self.update_callback = update_callback
        self.crawler_manager = smthread.SMThreadManager(max_threads=8, func=self._crawl)
        self.parser_manager = smthread.SMThreadManager(max_threads=2, func=self._parse)
        self.login = login.Login()
        self.links_queue = Queue.Queue()
        self._parser = parser
        self._crawler = cralwer
        self._checker = url_check.BloomFilter(item_count=10000, prob=0.01)

    def start(self, init_urls):
        self.login.check()
        for url in init_urls:
            self.crawler_manager.do(url)
        self.logger.info("Starting to Crawl")
        while True:
            try:
                urls = self.links_queue.get(timeout=1)
                urls = url_check.check_urls(urls, self._checker)
                for url in urls:
                    self.crawler_manager.do(url)
            except Queue.Empty:
                continue

    def _parse(self, args):
        """
        解析出内容和url
        :param content:
        :return:
        """
        url, content = args
        content_type = url_check.get_url_type(url)
        content_type, links, content = self._parser(content_type, content)
        if len(links):
            self.links_queue.put(links)
        store.save_file(content_type, content)
        if self.update_callback:
            self.update_callback(content_type)
        self.logger.info("[Parser] Finish parsing %s" % url)

    def _crawl(self, url):
        """
        Get content
        :param url:
        :return:
        """
        content = self._crawler(url)
        if content is not None:
            self.parser_manager.do((url, content))
            self.logger.info("[Crawler] Finish crawling %s" % url)
        else:
            self.crawler_manager.do(url)
            self.logger.warn("[Crawler] Crawler Failed %s" % url)

    def run(self):
        urls = [
            'https://www.zhihu.com/search?type=content&q=%E6%9C%AA%E9%97%BB%E8%8A%B1%E5%90%8D'

            # 'https://www.zhihu.com/question/26006703',
            # 'https://www.zhihu.com/topic',
            # 'https://www.zhihu.com/topic/19565870',
            # 'https://www.zhihu.com/topic/19550355',
            # 'https://www.zhihu.com/question/264580669',
            # 'https://www.zhihu.com/people/webto/',
            # 'https://www.zhihu.com/question/29130226/answer/284394337',
            # 'https://www.zhihu.com/question/30943322',
            # 'https://www.zhihu.com/question/52253320/answer/284550438',
        ]
        self.start(urls)

    def exit_app(self):

        exit(0)


def _parser(content_type, content):

    return parser.parse_html(content_type, content)


def _get_html(url):

    return gethtml.get_html(url)


def main():

    app = SpiderApplication(_parser, _get_html)
    urls = [
        'https://www.zhihu.com/search?type=content&q=%E6%9C%AA%E9%97%BB%E8%8A%B1%E5%90%8D'
        # 'https://www.zhihu.com/question/26006703',
        # 'https://www.zhihu.com/topic',
        # 'https://www.zhihu.com/topic/19565870',
        # 'https://www.zhihu.com/topic/19550355',
        # 'https://www.zhihu.com/question/264580669',
        # 'https://www.zhihu.com/people/webto/',
        # 'https://www.zhihu.com/question/29130226/answer/284394337',
        # 'https://www.zhihu.com/question/30943322',
        # 'https://www.zhihu.com/question/52253320/answer/284550438',
    ]
    app.start(urls)


# if __name__ == '__main__':
#     main()
