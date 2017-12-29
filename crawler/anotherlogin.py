# -*- coding: utf-8 -*-
from selenium import webdriver
from common import common
import time
import sys
sys.path.append('../')

if common.check_system() == 'macOS':
    exec_path = './phantomjs/phantomjs'
else:
    exec_path = './phantomjs/phantomjs.exe'
driver = webdriver.PhantomJS(exec_path)
driver.set_page_load_timeout(20)
driver.get('https://www.zhihu.com/')

account = raw_input('请输入你的用户名\n>  ')
secret = raw_input("请输入你的密码\n>  ")
email = driver.find_element_by_xpath("//input[@name='username']")
email.clear()
email.send_keys(account)
password = driver.find_element_by_xpath("//input[@name='password']")
password.clear()
password.send_keys(secret)
driver.find_element_by_class_name("SignFlow-submitButton").click()
time.sleep(3)
html = driver.page_source
driver.get_cookies()
print html
driver.quit()