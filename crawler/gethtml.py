# -*- coding: utf-8 -*-
import time
import os
import sys
sys.path.append('../')
from common import common
import requests
from selenium import webdriver

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
    "Referer": "http://www.zhihu.com/",
    'Host': 'www.zhihu.com',
}


def get_html(url, keyword=""):
     try:

        url = url.split('/answer')[0]
        print(len(keyword))
        if len(keyword) > 1:
            keywords = {'q': keyword}
            r = requests.get(url, params=keywords, headers=headers)
            url = url+"q="+keyword
        else:
            r = requests.get(url, headers=headers)

        r.raise_for_status()
        r.encoding = r.apparent_encoding
        # 需要提供运行机器上PhantomJS/firefox执行地址
        # host添加127.0.0.1 localhost
        service_args = []
        # 关闭图片加载
        service_args.append('--load-images=no')
        # 开启缓存
        service_args.append('--disk-cache=yes')
        if common.check_system() == 'macOS':
            exec_path = './phantomjs/phantomjs'
        else:
            exec_path = './phantomjs/phantomjs.exe'
        driver = webdriver.PhantomJS(exec_path,service_args=service_args)
        # # 设置超时时间
        driver.implicitly_wait(30)
        driver.set_page_load_timeout(30)
        #driver.get("https://www.zhihu.com/settings/profile")
        # with open('zhihucookie', 'r') as cookies:
        #     print(cookies.read())
        #     print("-------")
        #     driver.add_cookie(cookies.read())
        #     cookies.close()

        driver.get(url)
        # driver.get("https://www.zhihu.com/settings/profile")
        # html = driver.page_source
        # print(html)
        time.sleep(0.5)
        for i in range(2):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
        html = driver.page_source
        print (html)
        # # session_token = re.findall(r'session_token=([0-9,a-z]{32})', r.text)[0]
        # auto = re.findall(r'carCompose&quot;:&quot;(.*?)&quot', r.text)[0]
        # print(session_token)
        driver.quit()
     except:
        print ("crawl failed")

def main():
    keyword = "Vic Chan"
    url = "https://www.zhihu.com/search?"
    # keyword = ""
    # url = "https://www.zhihu.com/question/65483475/answer/261582944"
    get_html(url,keyword)

main()