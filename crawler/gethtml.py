# -*- coding: utf-8 -*-
import time
import cookielib
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
        #print(len(keyword))

        if url.find("zhihu.com/people") != -1 :
            r = requests.get(url, headers=headers)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.text

        if len(keyword) > 1:
            #keywords = {'q': keyword}
            #r = requests.get(url, params=keywords, headers=headers)
            url = url+"q="+keyword

        # 需要提供运行机器上PhantomJS执行地址
        # host添加127.0.0.1 localhost
        service_args = []
        # 关闭图片加载
        service_args.append('--load-images=no')
        # 开启缓存
        service_args.append('--disk-cache=yes')
        system = common.check_system()
        if system == 'macOS':
            exec_path = 'crawler/phantomjs/phantomjs'
        elif system == 'linux':
            exec_path = 'crawler/phantomjs/phantomjs_linux'
        else:
            exec_path = 'crawler/phantomjs/phantomjs.exe'
        driver = webdriver.PhantomJS(exec_path,service_args=service_args)
        # # 设置超时时间
        driver.implicitly_wait(50)
        driver.set_page_load_timeout(40)
        #非问题页面需要登录知乎查看
        if url.find("question") == -1 :
            driver.get("https://www.zhihu.com")
            driver.delete_all_cookies()
            try:
                # 测试cookie
                load_cookies = cookielib.LWPCookieJar()
                load_cookies.load(filename='zhihucookie', ignore_discard=False, ignore_expires=False)
                cookies = requests.utils.dict_from_cookiejar(load_cookies)
                # print(cookies)
                for name,value in cookies.items():
                    # print("----------")
                    # print(name)
                    # print(value)
                    driver.add_cookie({
                    'name': name,
                    'value': value,
                    'path':'/',
                    'domain': '.zhihu.com',
                     })
            except:
                 # pass
                cookie1 = {
                    'name': 'cap_id',
                    'value':'\"OTMxMmFmNmRmYzhkNDlkZDgxNTYwNjU4NmY3NGM5ZjI=|1513698629|2dd5a1effdf15f6c62b29ab05974896c3cddefa1\"' ,
                    'path':'/',
                    'domain': '.zhihu.com',
                    'expires': '2018-01-18 15:50:29Z',
                    'version': 0
                }
                cookie2 = {
                    'name': 'q_c1',
                    'value':'\"84f083b94bde45cd8ac315a1bd838602|1513698629000|1513698629000' ,
                    'path':'/',
                    'domain': '.zhihu.com',
                    'expires': '2018-01-18 15:50:29Z',
                    'version': 0
                }
                cookie3 = {
                    'name': 'r_cap_id',
                    'value':'\"OTMxNGY2MTk4ZmE2NDM3OWI2ZWJhODk1NjgxNmFhZjg=|1513698629|93d57f86473d37de8c7876949fecf6455539fdd5\"' ,
                    'path':'/',
                    'domain': '.zhihu.com',
                    'expires': '2018-01-18 15:50:29Z',
                    'version': 0
                }
                cookie4 = {
                    'name': 'z_c0',
                    'value':'\"MS4xY25YRkFRQUFBQUFYQUFBQVlRSlZUVnlESmx1VkdReWxVUjZhbm1Jd0hRUFNjM0FVNWdiV09BPT0=|1513698652|56e298ed1f4f73655cce6bdac7c9f2df1c21ee0a\"' ,
                    'path':'/',
                    'domain': '.zhihu.com',
                    'expires': '2018-01-18 15:50:29Z',
                    'version': 0
                }
                driver.add_cookie(cookie1)
                driver.add_cookie(cookie2)
                driver.add_cookie(cookie3)
                driver.add_cookie(cookie4)

        # driver.get(url)
        # driver.get("https://www.zhihu.com/settings/profile")
        # html = driver.page_source
        # print(html)
        driver.get(url)
        time.sleep(0.5)
        for i in range(5):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
        html = driver.page_source
        driver.quit()
        return html
    except:
        print ("crawl failed")
        return None


def main():
    keyword = "Vic Chan"
    url = "https://www.zhihu.com/search?"
    # keyword = ""
    # url = "https://www.zhihu.com/question/65483475/answer/261582944"
    page = get_html(url,keyword)
# main()
