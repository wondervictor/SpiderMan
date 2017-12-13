import requests

def GetHTML(keyword):
    try:
        head = {'user-agent':'Mozilla/5.0'}
        keyword = {'q':keyword}
        #r = requests.get("https://www.zhihu.com/search?",params= keyword, headers = head)
        r = requests.get("https://www.zhihu.com",headers=head)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        print(r.text[:1000])
    except:
        print("faile")

def main():
    keywords = "Victor Chan"
    GetHTML(keywords)

main()