from src.app_spider.utils import get_url_content, save_to_redis, save_to_mongodb,filter_emoji,get_redis_conn,random_sleep
import json


def main():
    create_url_list(10)
    for url in get_url_list():
        # 随机睡眠
        random_sleep()
        print('华为应用商店')
        print('正在获取当前华为应用商城{}app的信息'.format(url))
        content = get_url_content(url, 'get')
        content = json.loads(content)
        apps = content['layoutData'][0]['dataList']
        app_data_list = []
        huawei_keys = ['appid', 'name', 'intro', 'downCountDesc', 'score', 'tagName', 'downurl']
        keys = ['appId', 'appName', 'description', 'appDownCount', 'averageRating', 'categoryName', 'apkUrl']
        for app in apps:
            app_data = {}
            for key in keys:
                app_data[key] = app[huawei_keys[keys.index(key)]]
                app_data['source'] = '华为'
                app_data['auth_info'] = get_auth()
            save_to_redis({'appId': app['appid'], 'appName': app['name']})
            app_data_list.append(app_data)
            save_comment(app['appid'])
        save_to_mongodb(app_data_list)


def save_comment(app_id):
    for page_count in range(1, 4):
        url = "https://web-drcn.hispace.dbankcloud.cn/uowap/index?method=internal.user.commenList3&serviceType=20&reqPageNum=" + str(
            page_count) + "&maxResults=25&appid=" + str(app_id) + "&zone=&locale=zh_CN"

        content = get_url_content(url,'get')
        content = json.loads(content)
        comments = content['list']
        keys = ['commentId', 'commentInfo', 'stars']
        for comment in comments:
            comment_data = {}
            for key in keys:
                if key=='commentInfo':
                    comment_data[key] = filter_emoji(comment[key])
                    comment_data['app_store'] = '华为'
                    comment_data['appId'] = app_id
                else:
                    comment_data[key] = comment[key]
                    comment_data['app_store'] = '华为'
                    comment_data['appId'] = app_id
            save_to_mongodb([comment_data], comment=True)


def get_auth():
    return ''


def create_url_list(page=10):
    url = 'https://web-drcn.hispace.dbankcloud.cn/uowap/index?method=internal.getTabDetail&serviceType=20&reqPageNum={}&uri=33ef450cbac34770a477cfa78db4cf8c&maxResults=25&zone=&locale=zh'
    for i in range(1, page):
        temp_url =  url.format(i)
        redis_conn = get_redis_conn(0)
        redis_conn.lpush('request_url:2', url)

def get_url_list():

    redis_conn  = get_redis_conn(0)
    return redis_conn.lrange('request_url:2',0,-1)



if __name__ == '__main__':
    main()
