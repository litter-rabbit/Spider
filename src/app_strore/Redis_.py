import json
import time

import redis
from redis import StrictRedis

#pool = redis.ConnectionPool(host='10.13.88.111',port = 6379, db =0)
pool = redis.ConnectionPool(host='127.0.0.1',port = 6379, db =0)
pool2 = redis.ConnectionPool(host='127.0.0.1',port = 6379, db =2)


def Set_Request_Url(dict_data):
    conn = StrictRedis(connection_pool=pool)
    conn.rpush("RequestList", str(dict_data))
    print('{}连接存入redis成功'.format(str(dict_data)))
    return True


def save_app_info(dict_data):
    conn = StrictRedis(connection_pool=pool2)
    is_have=Search_url_id(dict_data["appId"])
    if not is_have:
        conn.sadd('appIds',dict_data['appId'])
        conn.lpush('appNames',dict_data['appName'])
        print('存入appId和appName')
    else:
        print(dict_data)
    return True


def Search_Request_Url(sort,app_store,request_type):
    results=[]
    conn = StrictRedis(connection_pool=pool)
    lists=conn.lrange("RequestList",0,-1)
    #print(lists)
    for url in lists:
        data = eval(str(url.decode('utf-8')))
        if str(data['sort'])==str(sort) and data['app_store']==app_store and data['request_type']==request_type:
            results.append(data['url'])
    return results



def Search_url(urls,num):
    results=[]
    conn = StrictRedis(connection_pool=pool)
    urlst = conn.lrange("RequestList", 0, num)
    all=conn.llen('RequestList')
    for url in urlst:
        data=eval(str(url.decode('utf-8')))
        if str(data['url']) == str(urls):
            results.append(data['url'])
    if len(results)==1:
        return results
    else:
        num+=10000
        if all<num:
            return []
        else:
             return  Search_url(urls,num)

def Search_url_id(ID):
    results=[]
    num=10000
    conn = StrictRedis(connection_pool=pool)
    urlst = conn.lrange("infos", 0, num)
    all=conn.llen('infos')
    for url in urlst:
        data=eval(str(url.decode('utf-8')))
        if str(data['appId']) == str(ID):
            results.append(data['appId'])
    if len(results)==1:
        return True
    else:
        num+=10000
        if all<num:
            return False
        else:
             return  Search_url(ID)
    return False