import requests
import execjs
import ctypes
# @mnuXbO3i7
headers = {
    'cookie':'uin=o0709343607; skey=@MSnwGKhcy; p_uin=o0709343607;p_skey=4T2dhZxKT668mi5Ql-Jakkc7Np7IfLesnT4L-3CdBkY_;',

}

url = 'https://qun.qq.com/cgi-bin/qun_mgr/get_group_list'


"""
o.data.bkn = function() {
        for (var e = $.cookie("skey"), t = 5381, n = 0, o = e.length; n < o; ++n)
            t += (t << 5) + e.charAt(n).charCodeAt();
        return 2147483647 & t
    }();

"""

def get_bkn1(skey):
    e=skey

    t=5381
    n=0
    o=len(e)
    while n<o:
        t+= (ctypes.c_int(t<<5).value+ord(e[n]))
        n += 1
    return 2147483647 & t



def get_bkn(skey):
    bkn=execjs.compile("""
        function get(skey) {
        for (var e = skey, t = 5381, n = 0, o = e.length; n < o; ++n)
            t += (t << 5) + e.charAt(n).charCodeAt();
           
       // return 2147483647 & t
        return t    
         
    };
    """)

    return (bkn.call("get",skey))


import re
def get_skey():
    cookie='uin=o0709343607; skey=@MSnwGKhcy; p_uin=o0709343607;p_skey=4T2dhZxKT668mi5Ql-Jakkc7Np7IfLesnT4L-3CdBkY_;'
    res=re.search('uin=(.*?);',cookie).group(1)
    return res[2:]





import sys
import json
def run():

    data = {
        "bkn": "157539168"
    }
    res = requests.post(url=url, headers=headers, data=data)
    print(res.status_code)
    res=res.content.decode('utf-8')
    res=json.loads(res)

    print(res)



if __name__ == '__main__':
    print(get_skey())
