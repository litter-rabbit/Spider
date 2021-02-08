

import requests
from time import time
from random import sample,randint
import hashlib


# 主要要找到生成url规则的js代码

def get(url):
    response=requests.request('GET',url)
    print(response.text)



def hex5(value):
    m=hashlib.md5()
    m.update(value.encode('utf-8'))
    return m.hexdigest()


def url():
    actions="".join([str(randint(1,9)) for x in range(5)])
    tim=str(round(time()))
    randstr="".join([chr(randint(65,91)) for x in range(5)])
    sign=hex5(actions+tim+randstr)
    base_url='http://www.porters.vip/verify/sign/fet?'
    uri='actions={}&tim={}&randstr={}&sign={}'.format(actions,tim,randstr,sign)

    return base_url+uri

import time

def task(a):
    time.sleep(1)
    print(a)

from multiprocessing import Pool
if __name__ == '__main__':
    p=Pool()
    a=input('输入')

    while a=='1':
        p.apply(task,args=('进程开始',))

        a=input('输入')


