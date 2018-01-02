# -*- coding: utf-8 -*-
import requests
import cookielib
import json
import re
import time
import os.path
# from bs4 import BeautifulSoup
try:
    from PIL import Image
except:
    pass

# 构造 Request headers
headers = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    "User-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
}


# 使用登录cookie信息
class Login(object):

    def __init__(self):
        self._init_session()

    def _init_session(self):
        self._session = requests.session()
        self._session.cookies = cookielib.LWPCookieJar(filename='crawler/zhihucookie')
        try:
            self._session.cookies.load(ignore_discard=True)
        except:
            print('cookie 文件未能加载')

    def check(self):

        if self.is_login():
            print('您已经登录')
        else:
            account = raw_input('请输入你的用户名\n>  ')
            secret = raw_input("请输入你的密码\n>  ")
            self.login(secret, account)

    def _get_xsrf(self):
        """
        _xsrf 是一个动态变化的参数
        """
        index_url = 'https://www.zhihu.com/#signin'
        # 获取登录时需要用到的_xsrf
        index_page = requests.get("https://www.zhihu.com/#signin", headers=headers)
        index_page.raise_for_status()
        index_page.encoding = index_page.apparent_encoding
        html = index_page.text
        # print(html[:10000])
        pattern = r'name="_xsrf" value="(.*?)"'
        # 这里的_xsrf 返回的是一个list
        _xsrf = re.findall(pattern, html)
        return _xsrf[0]

    # 获取验证码
    def _get_captcha(self):
        t = str(int(time.time() * 1000))
        captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
        r = self._session.get(captcha_url, headers=headers)
        with open('captcha.jpg', 'wb') as f:
            f.write(r.content)
            f.close()
        # 用pillow 的 Image 显示验证码
        # 如果没有安装 pillow 到源代码所在的目录去找到验证码然后手动输入
        try:
            im = Image.open('captcha.jpg')
            im.show()
            im.close()
        except:
            print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))

        sig = raw_input('验证码类型，字符1，倒立汉字2:')
        if sig == '1':
            captcha = raw_input('请输入验证码：')
        else:
            captcha = {
                'img_size': [200, 44],
                'input_points': [],
            }
            points = [[22.796875, 22], [42.796875, 22], [63.796875, 21], [84.796875, 20], [107.796875, 20],
                      [129.796875, 22],
                      [150.796875, 22]]
            seq = raw_input('请输入倒立字的位置:')
            for i in seq:
                captcha['input_points'].append(points[int(i) - 1])
            captcha = json.dumps(captcha)
        return captcha

    def is_login(self):
        # 通过查看用户个人信息来判断是否已经登录
        url = "https://www.zhihu.com/settings/profile"
        login_code = self._session.get(url, headers=headers, allow_redirects=False).status_code
        # profile_response = self._session.get(url, headers=headers, allow_redirects=False)
        # profile_soup = BeautifulSoup(profile_response.text, 'html.parser')
        # print (profile_response.text)
        if login_code == 200:
            return True
        else:
            return False

    def login(self, secret, account):
        _xsrf = self._get_xsrf()
        headers["X-Xsrftoken"] = _xsrf
        headers["X-Requested-With"] = "XMLHttpRequest"
        # 通过输入的用户名判断是否是手机号
        if re.match(r"^1\d{10}$", account):
            print("手机号登录 \n")
            post_url = 'https://www.zhihu.com/login/phone_num'
            post_data = {
                '_xsrf': _xsrf,
                'phone_num': account,
                'password': secret,
                'captcha_cn': 'cn'
            }
        else:
            if "@" in account:
                print("邮箱登录 \n")
            else:
                print("你的账号输入有问题，请重新登录")
                return
            post_url = 'https://www.zhihu.com/login/email'
            post_data = {
                '_xsrf': _xsrf,
                'email': account,
                'password': secret,
                'captcha_cn': 'cn'
            }
        # 不需要验证码直接登录成功
        login_response = self._session.post(url=post_url, headers=headers, data=post_data)
        login_response.encoding = login_response.apparent_encoding
        print('loginresponse', login_response.status_code)
        # print(login_response.json())
        # 验证码问题输入导致失败: 猜测这个问题是由于session中对于验证码的请求过期导致
        while login_response.json()['r'] == 1:
            # 不输入验证码登录失败
            # 使用需要输入验证码的方式登录
            post_data["captcha"] = self._get_captcha()
            login_page = self._session.post(post_url, data=post_data, headers=headers)
            login_code = login_page.json()
            print(login_code['msg'])
        # 保存 cookies 到文件，
        # 下次可以使用 cookie 直接登录，不需要输入账号和密码
        self._session.cookies.save()


# if __name__ == '__main__':
#
#     login = Login()
#     login.check()
