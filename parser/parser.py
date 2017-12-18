# -*- coding: utf-8 -*-

"""
Parser
"""

from bs4 import BeautifulSoup


def base_parse(html_str):

    """
    :param html_str: html to parse
    :return:
    """
    pass


def add_prefix(url):

    """
    add [www.zhihu.com] prefix to the parsed links
    :param url:
    :return:
    """
    host = "www.zhihu.com"

    def add(x):
        if "http" in x:
            return x
        else:
            return host + x

    if type(url) == list:
        url = map(add, url)
    else:
        url = host + url

    return url


def parse_links(html_str):

    """
    :param html_str:
    :return: List [link]
    """
    def filter_urls(url):
        others = ['javascript:;', '/settings', '/jobs','/app','/jubao','/contact','/terms', '/inbox','www.zhihu.com/inbox', '/logout', '/','www.zhihu.com/', 'notifications']
        if url in others or '#' in url:
            return False
        return True

    html = BeautifulSoup(html_str, 'html.parser')
    links = set()
    for a in html.find_all('a', href=True):
        if a.get_text(strip=True):
            links.add(a['href'])
    links = filter(filter_urls, links)
    links = add_prefix(links)
    print('Overall Links Num: %s' % len(links))
    return links


def parse_topics():

    """
    parse topics in [www.zhihu.com/topic/]
    :return:
    """

    pass


def parse_session_token(html_str):

    pass


def __test__parse_links__():

    html_file_path = 'test/topic19959450.html'
    content = open(html_file_path, 'r').read().decode('utf-8')
    links = parse_links(content)
    return links


# __test__parse_links__()

