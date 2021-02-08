

import requests

def post(url,data,headers):

    reponse=requests.post(url,data=data,headers=headers)
    print(reponse.text)



"""
i: 你好
from: AUTO
to: AUTO
smartresult: dict
client: fanyideskweb
salt: 15872104424524
sign: 3a09161af56389897c194686d0dce2a7
ts: 1587210442452
bv: aba2eb413aab2b3c6b790cc4b2ce2dc8
doctype: json
version: 2.1
keyfrom: fanyi.web
action: FY_BY_REALTlME

"""
def md5(value):
    import hashlib
    m=hashlib.md5()
    m.update(value.encode('utf8'))
    return m.hexdigest()

def get_data(content):
    import time
    from random import randint
    appversion='5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'


    ts=str(int(time.time()*1000))
    salt=ts+str(randint(0,10))
    bv=md5(appversion)
    sign=md5("fanyideskweb" + content + salt + "Nw(nmmbP%A-r6U3EUn]Aj")

    data={
        'i':content,
        'from': 'AUTO',
        'tp':'AUTO',
        'smartresult':'dict',
        'client':'fanyideskweb',
        'salt':salt,
        'sign':sign,
        'ts':ts,
        'bc':bv,
        'doctype':'json',
        'version':'2.1',
        'keyfrom':'fanyi.web',
        'action':'FY_BY_REALTlME'

    }
    return  data


if __name__ == '__main__':
    content=input('请输入翻译内容')
    data=get_data(content)
    url='http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    headers = {

        "Cookie": "OUTFOX_SEARCH_USER_ID=-269532254@61.164.45.178; OUTFOX_SEARCH_USER_ID_NCOO=319595972.4533894; JSESSIONID=aaavbU6zTTPKSanbz2H_w; ___rl__test__cookies=1578968436936",
        "Referer": "http://fanyi.youdao.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36" ,

    }

    post(url,data,headers=headers)




