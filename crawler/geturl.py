# -*- coding: utf-8 -*-
import requests

def GetHTML(url,keyword):
    try:
        head = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
        keyword = {'q':keyword}
        url = url.split('/answer')[0]
        #print(url)
        if len(keyword)> 0:
            r = requests.get(url,params= keyword, headers = head)
        else:
            r = requests.get(url,headers=head)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        print(r.text)
    except:
        print("faile")

def main():
    keyword = "Vic Chan"
    url = "https://www.zhihu.com/search?"
    #url = "https://www.zhihu.com/question/35855905/answer/261582944"
    GetHTML(url,keyword)

main()