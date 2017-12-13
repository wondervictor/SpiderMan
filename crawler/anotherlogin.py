# coding: utf8

import requests
from bs4 import BeautifulSoup
import os, time
import re
# import http.cookiejar as cookielib

# 构造 Request headers
agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'
headers = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    'User-Agent': agent
}

head = {'user-agent':'Mozilla/5.0'}

######### 构造用于网络请求的session
session = requests.Session()
# session.cookies = cookielib.LWPCookieJar(filename='zhihucookie')
# try:
#     session.cookies.load(ignore_discard=True)
# except:
#     print('cookie 文件未能加载')

############ 获取xsrf_token
index_page = requests.get("https://www.zhihu.com/#signin", headers=head)
index_page.raise_for_status()
index_page.encoding = index_page.apparent_encoding
html = index_page.text
pattern = r'name="_xsrf" value="(.*?)"'
_xsrf = re.findall(pattern, html)
########## 获取验证码文件
randomtime = str(int(time.time() * 1000))
captchaurl = 'https://www.zhihu.com/captcha.gif?r='+\
             randomtime+"&type=login"
captcharesponse = session.get(url=captchaurl, headers=headers)
with open('checkcode.gif', 'wb') as f:
    f.write(captcharesponse.content)
    f.close()
# os.startfile('checkcode.gif')
captcha = raw_input('请输入验证码：')
print(captcha)

########### 开始登陆
headers['X-Xsrftoken'] = _xsrf[0]
headers['X-Requested-With'] = 'XMLHttpRequest'
loginurl = 'https://www.zhihu.com/login/email'
postdata = {
    '_xsrf': _xsrf[0],
    'email': 'wonderstruclvictorz@hotmail.com',
    'password': 'vic19961108',
    'captcha_cn': 'cn'
}
loginresponse = session.post(url=loginurl, headers=headers, data=postdata)
print(loginresponse.status_code)
# print(loginresponse.json())
# 验证码问题输入导致失败: 猜测这个问题是由于session中对于验证码的请求过期导致

# if loginresponse.json()['r']==1:
#     # 重新输入验证码，再次运行代码则正常。也就是说可以再第一次不输入验证码，或者输入一个错误的验证码，只有第二次才是有效的
#     randomtime = str(int(time.time() * 1000))
#     captchaurl = 'https://www.zhihu.com/captcha.gif?r=' + \
#                  randomtime + "&type=login"
#     captcharesponse = session.get(url=captchaurl, headers=headers)
#     with open('checkcode.gif', 'wb') as f:
#         f.write(captcharesponse.content)
#         f.close()
#     os.startfile('checkcode.gif')
#     captcha = input('请输入验证码：')
#     print(captcha)
#
#     postdata['captcha'] = captcha
#     loginresponse = session.post(url=loginurl, headers=headers, data=postdata)
#     print('服务器端返回响应码：', loginresponse.status_code)
#     print(loginresponse.json())




##########################保存登陆后的cookie信息
#session.cookies.save()
############################判断是否登录成功
profileurl = 'https://www.zhihu.com/settings/profile'
profileresponse = session.get(url=profileurl, headers=headers)
print( profileresponse.status_code)
profilesoup = BeautifulSoup(profileresponse.text, 'html.parser')
print (profileresponse.text)
div = profilesoup.find('div', {'id': 'rename-section'})
print(div)