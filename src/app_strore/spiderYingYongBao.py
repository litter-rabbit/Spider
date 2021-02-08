# 爬取应用宝

import time
import requests
# from spiderApp import models
import json
import random

from Redis_ import Search_Request_Url, Search_url, Set_Request_Url,save_app_info
from models import Proxy, Brower, Appdata

g_appStore = "应用宝"


# 爬取地址
# orgame 1:全部应用; 2:全部游戏
# categoryId: 分类 0:全部分类
# pageSize 数据量:固定20
# pageContext 跳过多少数据:20的倍数
def spiderMain():
    """
    爬虫主体函数
    """
    print("\r\n\r\n\r\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    spiderSort2()
    spiderSort1()
    # 创建请求路径
    print("创建请求路径start")
    createUrlList(8)
    print("创建请求路径end")

    return True

def spiderSort2():
    urlList = getUrlList(sort=2)
    for url in urlList:
        # print(url)
        # try:
        # 随机睡眠, 模仿人
        # time.sleep(random.uniform(0, 0.5))
        # 获取数据库中的user-agent, 随机获取其中一个
        oneBrower = getOneBrower()
        # # 获取数据库中的代理, 随机获取其中一个
        # oneProxy = getOneProxy()
        headers = {
            "User-Agent": oneBrower["user_agent"]
        }
        free_proxy = {
            # bug, 代理分为http与https这里没有加以区分
            "https": ""#str(oneProxy["ip"]) + ":" + str(oneProxy["port"])
        }
        # 获取数据
        print('正在获取{}的信息'.format(url))
        response = requests.get(url, headers=headers, proxies=free_proxy,timeout=15)
        if response.status_code != 200:
            continue
        data_content = response.content.decode("utf-8")
        appJsonData = json.loads(data_content)
        if None == appJsonData["obj"] or False == appJsonData["success"]:
            continue
        res = handle1(appJsonData)
        # except Exception as e:
        #     print(e)
        #     pass

def spiderSort1():
    # 获取请求顺序为1的路径
    urlList = getUrlList(sort=1)
    for url in urlList:
        # print(url)
        try:
            # 随机睡眠, 模仿人
            # time.sleep(random.uniform(0, 1))
            # 获取数据库中的user-agent, 随机获取其中一个
            oneBrower = getOneBrower()
            # # 获取数据库中的代理, 随机获取其中一个
            # oneProxy = getOneProxy()
            headers = {
                "User-Agent": oneBrower["user_agent"]
            }
            free_proxy = {
                "https":""# str(oneProxy["ip"]) + ":" + str(oneProxy["port"])
            }
            # 获取数据
            response = requests.get(url, headers=headers, proxies=free_proxy,timeout=15)
            if response.status_code != 200:
                continue
            data_content = response.content.decode("utf-8")
            appJsonData = json.loads(data_content)
            if None == appJsonData["obj"] or False == appJsonData["success"] or 0 == len(appJsonData["obj"]):
                # print("通过该url获取空")
                continue
            # print("通过该url获取个数:",len(appJsonData["obj"]))
            res = handle2(appJsonData)

        except:
            pass

def handle2(appJsonData):
    """
    处理函数请求顺序为2的
    :param appJsonData:
    :return:
    """
    items = appJsonData["obj"]["items"]
    if None!=items:
        appJsonData = {}
        appJsonData["obj"] = [one["appDetail"] for one in items ]
    else:
        items = appJsonData["obj"]["appDetails"]
        appJsonData = {}
        appJsonData["obj"] = items
    return handle1(appJsonData)


def handle1(appJsonData):
    """
    处理函数1
    :param appJsonData:
    :return:
    """
    res = []
    # 将获取到的数据入库, 先查, 没有的进行写入, 有的进行更新
    for appObj in appJsonData["obj"]['items']:
        appObj=appObj['appDetail']
        appId = appObj["appId"]
        appName = appObj["appName"]
        description = "" if appObj["description"] == None else appObj["description"]
        appDownCount = appObj["appDownCount"]
        averageRating = appObj["averageRating"]
        categoryName = appObj["categoryName"]
        oneApp = {
            "appId": appId,
            "appName": appName,
            "description": description,
            "appDownCount": appDownCount,
            "averageRating": averageRating,
            "categoryName": categoryName,
        }
        save_app_info({'appId': appId, 'appName': appName})
        saveAppDataToDB(oneApp)
        res.append(oneApp)
    return res

def getOneBrower():
    qset = Brower.objects.all().values_list('user_agent')
    pl = list(set([one[0] for one in qset]))
    data = {'user_agent': pl[0]}
    return data

def getOneProxy():
    qset = Proxy.objects.all()
    num = random.randint(0, len(qset))
    data = {
        'ip': qset[num].ip,
        'port': qset[num].port,
    }
    return data

def createUrlList(pageSize=10):
    """
    按照一定规则生成url并放置在数据库中
    :return: list url数组
    """
    # 对于传进来的值进行判断, 如果非法, 重置成默认
    if None == pageSize:
        pageSize = 10
    pageSize = int(pageSize)
    if pageSize < 0:
        pageSize = -pageSize
    # 生成列表
    for page_count in range(pageSize):
        # 一页数量,固定20
        page_size = 20
        url = "https://sj.qq.com/myapp/cate/appList.htm?orgame=1&categoryId=0&pageSize=" + str(
            page_count * page_size) + "&pageContext=" + str((page_count + 1) * page_size)

        existUrl = len(Search_url(url,0))
        if existUrl > 0:
            continue
        data = {
            "app_store": g_appStore,
            "url": url,
            "sort": "1",
            "request_type": "get",
        }
        Set_Request_Url(data)
    # 获取已经存在的, list去重
    # 获取关键词, 拼接
    pns_sequences = ['', 'MTA', 'MjA', 'MzA', 'NDA', 'NTA', 'NjA', 'NzA', 'ODA', 'OTA', 'MTAw', 'MTEw', 'MTIw', 'MTMw','MTQw']
    for pns in pns_sequences:
        appKeywords = list(Appdata.objects.values_list("app_name", "category_name"))
        keywords = list(set([one[0] for one in appKeywords] + [one[1] for one in appKeywords]))
        for kw in keywords:
            url = "https://sj.qq.com/myapp/searchAjax.htm?kw="+str(kw)+"&pns="+str(pns)+"&sid="
            existUrl = len(Search_url(url,0))
            if existUrl > 0:
                continue
            data = {
                "app_store": g_appStore,
                "url": url,
                "sort": "2",
                "request_type": "get",
            }
            Set_Request_Url(data)
    return True


def getUrlList(sort=1):
    """
    获取urlList
    :return: []
    """
    app_store = g_appStore
    urlList = Search_Request_Url(sort, app_store, "get")
    return urlList


def saveAppDataToDB(oneApp):
    """
    将爬取到的数据存放到数据库中, 如果原本就存在, 进行更新, 不存在, 就创建
    :param oneApp: 一个APP的dir数据字典
    :return:
    """
    appId = oneApp["appId"]
    appName = oneApp["appName"]
    description = oneApp["description"]
    appDownCount = oneApp["appDownCount"]
    averageRating = oneApp["averageRating"]
    categoryName = oneApp["categoryName"]
    #     先看是否存在
    existApp = Appdata.objects.filter(
        app_id=str(appId),
        app_store=str(g_appStore),
    )
    # 如果存在, 就更新
    if len(existApp) > 0:
        existApp = list(existApp)
        # 简介不要被覆盖没有了
        if 0 == len(description):
            description = str(existApp[0].description)

        Appdata.objects.filter(
            app_id=str(appId),
            app_store=str(g_appStore),
        ).update(
            app_name=appName,
            description=description,
            app_down_count=str(appDownCount),
            average_rating=averageRating,
            category_name=categoryName,
        )
        print("更新:", g_appStore, "|", appId, "|", appName)
        return True
        # 不存在就插入
    else:
        # print("创建:",g_appStore,"|",appId,"|",appName)
        Appdata(
            app_id=str(appId),
            app_store=str(g_appStore),
            app_name=appName,
            description=description,
            app_down_count=str(appDownCount),
            average_rating=averageRating,
            category_name=categoryName,
        ).save()
        print("插入:", g_appStore, "|", appId, "|", appName)
        return True
# createUrlList()
