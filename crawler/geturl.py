# -*- coding: utf-8 -*-
import requests

def GetHTML(keyword):
    try:
        head = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
        keyword = {'q':keyword}
        r = requests.get("https://www.zhihu.com/search?",params= keyword, headers = head)
        #r = requests.get("https://www.zhihu.com",headers=head)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        print(r.text)
    except:
        print("faile")

def main():
    keywords = "Vic Chan"
    GetHTML(keywords)

main()