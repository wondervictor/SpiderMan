# -*- coding: utf-8 -*-
import time

import requests
from selenium import webdriver

#import re
#import json

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
    "Referer": "http://www.zhihu.com/",
    'Host': 'www.zhihu.com',
}

def GetHTML(url,keyword):
    # try:
        #head = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
        keyword = {'q':keyword}
        url = url.split('/answer')[0]
        print(len(keyword))
        if len(keyword)> 1:
            r = requests.get(url,params= keyword, headers = headers)
        else:
            r = requests.get(url,headers=headers)

        r.raise_for_status()
        r.encoding = r.apparent_encoding
        #需要提供执行地址
        driver = webdriver.Firefox()
        cookie = driver.get_cookies()
        driver.get(url)
        for i in range(10):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
        html = driver.page_source
        print (html)
        # session_token = re.findall(r'session_token=([0-9,a-z]{32})', r.text)[0]
        # auto = re.findall(r'carCompose&quot;:&quot;(.*?)&quot', r.text)[0]
        # print(session_token)
    # except:
    #     print ("crawl faile")
    #

def main():
    #keyword = "Vic Chan"
    #url = "https://www.zhihu.com/search?"
    url = "https://www.zhihu.com/question/35855905/answer/261582944"
    GetHTML(url,"")

main()