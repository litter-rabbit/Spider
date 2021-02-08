import requests
from app_spider.db import get_redis_conn, get_mongodb
import emoji, re
import time, random
import random
conn = get_redis_conn(0)
mongo_conn = get_mongodb()


def get_url_content(url, method, data=None):
    method = str(method).lower()

    # 随机获取
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)',
        'User-Agent: Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+',
        'User-Agent: Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan',

    ]
    index = len(user_agents)
    headers = {
        "user-agent": user_agents[random.randint(0,index-1)]
    }

    if method == 'get':
        rsp = requests.get(url)
        if rsp.status_code == 200:
            return rsp.text
        else:
            raise ValueError('get请求失败{}'.format(url))

    if method == 'post':
        rsp = requests.post(url, headers=headers, data=data)
        if rsp.status_code == 200:
            return rsp.text
        else:
            raise ValueError('post请求失败'.format(url))


def save_to_redis(data):
    conn.sadd('appId', data['appId'])
    conn.rpush('appName', data['appName'])
    print('存入redis成功', data['appName'], data['appId'])


def save_to_mongodb(data, comment=False):
    for app_data in data:
        if comment:
            query_dict = {'commentId': app_data['commentId']}
        else:
            query_dict = {'appId': app_data['appId']}
        if (mongo_conn.count(query_dict)):
            mongo_conn.delete_one(query_dict)
            mongo_conn.insert_one(app_data)
    print('存入mongodb成功', data)


def filter_emoji(content):
    """
    过滤掉所有表情符号
    :param content:
    :return:
    """

    content = emoji.demojize(content)
    content = re.sub(r':(.*?):', '', content).strip()
    cont = None
    # 过滤字符串串中的表情包
    try:
        # Wide UCS-4 build
        cont = re.compile(u'['u'\U0001F300-\U0001F64F' u'\U0001F680-\U0001F6FF'u'\u2600-\u2B55]+')
    except re.error:
        # Narrow UCS-2 build
        cont = re.compile(u'('u'\ud83c[\udf00-\udfff]|'u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'u'[\u2600-\u2B55])+')
    return cont.sub(u'', content)


def random_sleep():
    time.sleep(random.randint(0,5))
