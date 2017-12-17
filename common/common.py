# -*- coding: utf-8 -*-

"""
Common Functions

"""


import time
import datetime


def get_timestamp():
    """
    获取UNIX时间戳
    :return: int
    """
    return int(time.time())


def time_to_str(timestamp):
    """
    将时间戳转换成[YYYY-MM-DD HH:mm:ss]格式
    :param timestamp: 时间戳
    :return:
    """
    return datetime.datetime.\
        fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")