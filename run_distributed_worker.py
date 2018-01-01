# -*- coding: utf-8 -*-
import argparse

from crawler import gethtml
from parser import parser as htmlparse
from worker import Worker, WorkerConfig, AUTH_KEY


def crawl_func(s):
    return gethtml.get_html(s)


def parse_func(content_type, content):

    return htmlparse.parse_html(content_type, content)


def test_worker(ip):

    config = WorkerConfig(
        name='worker',
        task_batchsize=2,
        crawler_threads=8,
        parser_threads=2,
        authkey=AUTH_KEY,
        address=(ip, 23333)
    )

    worker = Worker(config=config, crawler_func=crawl_func, parser_func=parse_func)

    worker.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--master_ip', type=str, default='0.0.0.0', help='Master IP')

    args = parser.parse_args()

    test_worker(args.master_ip)
