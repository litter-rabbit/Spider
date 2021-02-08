
import random
public_key = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCfqhg/SotY/yKAxm34WHht37RJNKdktcOKNedhCnUhG7R8zlojgzTT78ZTMhgiDBMGEqeSTqy/hYz1qDlvU8CGpkP7BnEaiDgvF9ddckK5UDchN0CXNHygRXfq+1ylF3kFZmNk/5/uj6UJ4A2hpPcfcjARbWGhAgLpiBSn2iFDCQIDAQAB"
import json
from src.frida.work import hook_by_file
from src.frida.work import active_by_activity_name,kill_by_actiity_name
import hashlib



script = hook_by_file('huihe.js','com.zuiai.hh')

def get_random_str():
    temp = "abcdefghijklmnopqrstuvwxyz0123456789"
    random_str=""
    for i in range(16):
        random_str += temp[random.randint(0, len(temp) - 1)]
    return random_str

def get():

    public_key = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCfqhg/SotY/yKAxm34WHht37RJNKdktcOKNedhCnUhG7R8zlojgzTT78ZTMhgiDBMGEqeSTqy/hYz1qDlvU8CGpkP7BnEaiDgvF9ddckK5UDchN0CXNHygRXfq+1ylF3kFZmNk/5/uj6UJ4A2hpPcfcjARbWGhAgLpiBSn2iFDCQIDAQAB"
    random_str = get_random_str()
    me = script.exports.getme(random_str, public_key)
    print('me----',me)

    pwd = hashlib.md5(b'love201').hexdigest()
    gson = {"code":"%2B86","mobile":"1834135404","deviceData":"Xiaomi MI 8 SE 10","tokenUuid":"d3cc03ed-8fb2-30fa-b0d6-d6d7fe0e20d8","pwd":pwd,"isManualLogin":"1","version":"3.1.0","device":"1"}
    md = script.exports.getmd(json.dumps(gson), random_str)
    print('md---', md)
    return me,md


def login():
    url ="https://gateway-01.huihe2.com:9000/chat/user/doLogin"
    import requests
    me,md = get()
    data={
        'm_e':me,
        'm_d':md
    }
    headers={
    "user-agent":"okhttp/4.7.2"
    }
    res = requests.post(url=url,data=data,headers=headers,verify=False)

    print(res.text)
    print(res.json())


if __name__ == '__main__':
    while True:
        i = input()
        if i=='1':
            login()

