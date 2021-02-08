import requests
from requests.exceptions import ConnectionError




base_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
}

"""
    获取url的具体页面内容
"""
def get_content(url, options={}, proxies={}, verify=True):

    headers=dict(base_headers,**options)
    print('正在抓取',url)
    try:
        reponse=requests.get(url,headers=headers,proxies=proxies,verify=verify)
        if reponse.status_code==200:
            # 返回网页的具体内容
            return reponse.text
    except ConnectionError:
        print("抓取失败",url)
        return None


def ocr_num():
    pass









