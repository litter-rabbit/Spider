# 爬取应用宝

import time
import requests
# from spiderApp import models
import json
import random
import emoji,re

from Redis_ import Set_Request_Url, Search_Request_Url, Search_url,save_app_info
from models import Proxy, Comment, Brower, Appdata

g_appStore = "华为"


def spiderMain(#request
):
    """
    爬虫主体函数
    """
    # print("\r\n\r\n\r\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    # 创建请求路径

    spiderSort1()
    spiderSort2()

    # 创建评论url
    createCommentUrlList(3)
    spiderSort3()
    print("创建请求路径start")
    createUrlList(9)
    print("创建请求路径end")

    # return JsonResponse({"res": "爬取完毕"}, json_dumps_params={'ensure_ascii': False})
    return True

def spiderSort1():
    """
    爬取排序为1的链接,
    :return:
    """
    #     # 获取请求顺序为1的路径
    urlList = getUrlList(sort=1)
    for url in urlList:
        try:
            # 随机睡眠, 模仿人
            # time.sleep(random.uniform(0, 0.3))
            # 获取数据库中的user-agent, 随机获取其中一个
            oneBrower = getOneBrower()
            # # 获取数据库中的代理, 随机获取其中一个
            # oneProxy = getOneProxy()
            headers = {
                "User-Agent": oneBrower["user_agent"]
            }
            free_proxy = {
                # bug, 代理分为http与https这里没有加以区分
                "https": ""  # str(oneProxy["ip"]) + ":" + str(oneProxy["port"])
            }
            # 获取数据
            print('正在获取{}的信息，排序1'.format(url))
            response = requests.get(url, headers=headers, proxies=free_proxy, timeout=15)
            if response.status_code != 200:
                continue
            data_content = response.content.decode("utf-8")
            appJsonData = json.loads(data_content)
            # print(appJsonData)
            if None == appJsonData["layoutData"] or 0 == len(appJsonData["layoutData"]):
                continue
            dataList = [onedataList for onelayoutData in appJsonData["layoutData"] for onedataList in
                        onelayoutData["dataList"]]
            res = handle1(dataList)
        except Exception as e:
            print(e)
            # print(url,'  sort=1 ', "报错")
            pass

def spiderSort2():
    # 获取请求顺序为2的路径
    # 一页是一个详情
    urlList = getUrlList(sort=2)
    for url in urlList:
        try:
            # 随机睡眠, 模仿人
            # time.sleep(random.uniform(0, 0.3))
            # 获取数据库中的user-agent, 随机获取其中一个
            oneBrower = getOneBrower()
            # # 获取数据库中的代理, 随机获取其中一个
            # oneProxy = getOneProxy()
            headers = {
                "User-Agent": ""  # oneBrower["user_agent"]
            }
            free_proxy = {
                "https": ""  # str(oneProxy["ip"]) + ":" + str(oneProxy["port"])
            }
            # 获取数据
            print('正在获取{}的信息，排序 2'.format(url))
            response = requests.get(url, headers=headers, proxies=free_proxy,timeout=15)
            if response.status_code != 200:
                continue
            data_content = response.content.decode("utf-8")
            appJsonData = json.loads(data_content)
            if None == appJsonData["layoutData"] or 0 == len(appJsonData["layoutData"]):
                # print("通过该url获取空")
                continue
            res = handle2(appJsonData)
        except:
            # print(url,"  sort=2","报错")
            pass


def spiderSort3():
    """
    爬取顺序为3的, 主要是评论
    :return:
    """
    urlList = getUrlList(sort=3)
    # urlList = urlList[0:10]
    for url in urlList:
        try:
            # 随机睡眠, 模仿人
            # time.sleep(random.uniform(0, 0.5))
            # 获取数据库中的user-agent, 随机获取其中一个
            oneBrower = getOneBrower()
            # # 获取数据库中的代理, 随机获取其中一个
            oneProxy = getOneProxy()
            headers = {
                "User-Agent": ""  # oneBrower["user_agent"]
            }
            free_proxy = {
                # bug, 代理分为http与https这里没有加以区分
                "https": ""  # str(oneProxy["ip"]) + ":" + str(oneProxy["port"])
            }
            # 获取数据
            print('正在获取{}的信息，排序3'.format(url))
            response = requests.get(url, headers=headers, proxies=free_proxy,timeout=15)
            if response.status_code != 200:
                continue
            data_content = response.content.decode("utf-8")
            appJsonData = json.loads(data_content)
            if None == appJsonData["list"] or 0 == len(appJsonData["list"]):
                continue
            commentList = appJsonData["list"]
            res = handle3(commentList)
        except:
            # print(url,'   sort=3',"报错")
            pass

def handle3(commentList):#ok
    """
    处理评论
    :param commentList:
    :return:
    """
    for oneComment in commentList:
        commentId = str(oneComment["commentId"])
        appStore = g_appStore
        appId = str(oneComment["commentAppId"])
        commentInfo = filter_emoji(str(oneComment["commentInfo"]))
        stars = str(oneComment["stars"])
        existComment =Comment.objects.filter(comment_id=commentId, app_store=appStore)#.values("comment_id")
        # 该评论已经存在, 就不不必插入或者更新
        if len(existComment) > 0:
            print("已经存在评论")
            continue
        Comment(
            comment_id=commentId,
            app_store=appStore,
            app_id=appId,
            comment_info=commentInfo,
            stars=stars,
        ).save()


def filter_emoji(content):
    """
    过滤掉所有表情符号
    :param content:
    :return:
    """
    content = emoji.demojize(content)
    content = re.sub(r':(.*?):','',content).strip()
    cont=None
    # 过滤字符串串中的表情包
    try:
        # Wide UCS-4 build
        cont = re.compile(u'['u'\U0001F300-\U0001F64F' u'\U0001F680-\U0001F6FF'u'\u2600-\u2B55]+')
    except re.error:
        # Narrow UCS-2 build
        cont = re.compile(u'('u'\ud83c[\udf00-\udfff]|'u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'u'[\u2600-\u2B55])+')
    return cont.sub (u'', content)

def handle2(appJsonData):
    """
    处理函数请求顺序为2的
    一个请求是一个详情
    主要根据 layoutName 进行处理
    :param appJsonData:
    :return:
    """
    oneApp = {
        "appId": "",
        "appName": "",
        "description": "",
        "appDownCount": "",
        "averageRating": "",
        "categoryName": "",
    }
    for layout in appJsonData["layoutData"]:

        if "detailhiddencard" == layout["layoutName"]:
            oneApp["appId"] = layout["dataList"][0]["appid"]
        elif "detailheadcard" == layout["layoutName"]:
            oneApp["appName"] = layout["dataList"][0]["name"]
            oneApp["appDownCount"] = layout["dataList"][0]["intro"]

        elif "detailappintrocard" == layout["layoutName"]:
            oneApp["description"] = layout["dataList"][0]["appIntro"]
        elif "pcscorecommentlistcard" == layout["layoutName"]:
            for dataList in layout["dataList"]:
                if dataList["name"] == "评论":
                    oneApp["averageRating"] = dataList["list"][0]["score"]
    #  这里特殊写, 页面并没有分类, 自己从数据库获取一下
    dbAppdata = Appdata.objects.filter(app_id=oneApp["appId"], app_store=g_appStore)#.values("category_name"))
    if len(dbAppdata) == 0:
        return False
    oneApp["categoryName"] = dbAppdata[0]["category_name"]
    # print(oneApp)
    saveAppDataToDB(oneApp)


def handle1(dataList):
    """
    处理函数1
    :param dataList:
    :return:
    """
    res = []
    # 将获取到的数据入库, 先查, 没有的进行写入, 有的进行更新
    for appObj in dataList:
        appId = str(appObj["appid"])
        appName = str(appObj["name"])
        description = ""
        if "appIntro" in appObj:
            description = appObj["appIntro"]
        appDownCount = appObj["downCountDesc"]
        averageRating = appObj["score"]
        categoryName = appObj["tagName"]
        oneApp = {
            "appId": appId,
            "appName": appName,
            "description": description,
            "appDownCount": appDownCount,
            "averageRating": averageRating,
            "categoryName": categoryName,
        }
        save_app_info({'appId':appId,'appName':appName})
        saveAppDataToDB(oneApp)
        res.append(oneApp)
    return res


def getOneBrower():
    qset = Brower.objects.all()
    num = random.randint(0, len(qset)-1)
    data = {
        'user_agent': qset[num].user_agent,
    }
    return data

def getOneProxy():

    qset = Proxy.objects.all()
    num = random.randint(0, len(qset)-1)
    data = {
        'ip': qset[num].ip,
        'port': qset[num].port,
    }
    return data


def createUrlList(pageSize=8):
    """
    按照一定规则生成url并放置在数据库中
    :return: list url数组
    """
    # 对于传进来的值进行判断, 如果非法, 重置成默认
    if None == pageSize:
        pageSize = 8
    pageSize = int(pageSize)
    if pageSize < 0:
        pageSize = 8
    #  关键词列表 sort = 1
    appKeywordst = Appdata.objects.all().values_list("app_name", "category_name")
    key = [one[0] for one in appKeywordst] + [one[1] for one in appKeywordst]
    keywords = list(set(key))
    for kw in keywords:
        for page_count in range(1, pageSize):
            # 一页数量,固定
            page_size = 25
            # 拼接, 这是根据关键词搜索出来几页简单的
            url = "https://web-drcn.hispace.dbankcloud.cn/uowap/index?method=internal.getTabDetail&serviceType=20&reqPageNum=" + str(
                page_count) + "&uri=searchApp%7C" + str(kw) + "&maxResults=" + str(page_size) + "&zone=&locale=zh_CN"
            existUrl = len(Search_url(url,0))
            if existUrl > 0:
                continue
            data={
                "app_store":g_appStore,
                "url":url,
                "sort":"1",
                "request_type":"get",
            }
            Set_Request_Url(data)
    # 某个app的详情, 根据appid进行锁定, url sort = 2
    huaweiAppIds = list(Appdata.objects.filter(app_store=g_appStore).values_list("app_id"))
    appIds = list(set([one[0] for one in huaweiAppIds]))
    for appId in appIds:
        url = "https://web-drcn.hispace.dbankcloud.cn/uowap/index?method=internal.getTabDetail&serviceType=20&uri=app%7C" + str(
            appId) + "&appid=" + str(appId) + "&zone=&locale=zh_CN"
        existUrl = len(Search_url(url,0))
        if existUrl > 0:
            continue
        data={
            "app_store":g_appStore,
            "url":url,
            "sort":"2",
            "request_type":"get",
        }
        Set_Request_Url(data)
        print('生成请求连接成功')
    return True


def createCommentUrlList(pageSize=3):
    """
    按照一定规则生成评论的url列表
    :param pageSize:
    :return:
    """
    huaweiAppIds = list(Appdata.objects.filter(app_store=g_appStore).values_list("app_id"))
    appIds = list(set([one[0] for one in huaweiAppIds]))
    for appId in appIds:
        for page_count in range(1, pageSize + 1):
            url = "https://web-drcn.hispace.dbankcloud.cn/uowap/index?method=internal.user.commenList3&serviceType=20&reqPageNum=" + str(
                page_count) + "&maxResults=25&appid=" + str(appId) + "&zone=&locale=zh_CN"
            existUrl = len(Search_url(url,0))
            if existUrl > 0:
                continue
            data={
                "app_store":g_appStore,
                "url":url,
                "sort":"3",
                "request_type":"get",
            }
            Set_Request_Url(data)
            print('生成评论url成功')


def getUrlList(sort=1):
    """
    获取urlList
    :return: []
    """
    app_store=g_appStore
    urlList = Search_Request_Url(sort,app_store,"get")
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
    existApps = Appdata.objects.filter(
        app_id=str(appId),
        app_store=str(g_appStore),
    )
    # 如果存在, 就更新
    if len(existApps) > 0:
        existApp = list(existApps)
        if 0 == len(description):
            description = str(existApp[0].description)
        print("更新:", g_appStore, "|", appId, "|", appName)
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
        return True

    else:

        Appdata(
            app_id=str(appId),
            app_store=str(g_appStore),
            app_name=appName,
            description=description,
            app_down_count=str(appDownCount),
            average_rating=averageRating,
            category_name=categoryName,
        ).save()
        print("查润:", g_appStore, "|", appId, "|", appName)
        return True

#spiderMain()
