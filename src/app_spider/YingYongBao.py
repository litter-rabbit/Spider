from src.app_spider.utils import get_url_content, save_to_redis, save_to_mongodb, get_redis_conn,random_sleep
import json
import re


def main():
    create_url_list(10)
    for url in get_url_list():
        # 随机睡眠
        random_sleep()
        print('腾讯应用宝')
        print('正在获取腾讯应用宝{}下的app应用信息'.format(url))
        content = get_url_content(url, 'get')
        content = json.loads(content)
        apps = content["obj"]
        keys = ['appId', 'appName', 'description', 'appDownCount', 'averageRating', 'categoryName', 'apkUrl']
        app_list = []
        for app in apps:
            app_data = {}
            for key in keys:
                app_data[key] = app[key]
                app_data['auth_info'] = get_auth(app['pkgName'], app['apkMd5'])
                app_data['source'] = '腾讯'
            save_to_redis({'appId': app['appId'], 'appName': app['appName']})
            app_list.append(app_data)
        save_to_mongodb(app_list)


def get_auth(*args):
    url = 'https://sj.qq.com/myapp/detail.htm?apkName={}&info={}'.format(args[0], args[1])
    content = get_url_content(url, 'get')
    app_auths = re.findall(r'<li class="clearfix"><div class="l">-</div><div class="r">(.*?)</div></li>', content)
    return str(app_auths)


def create_url_list(page=10):
    for page_count in range(page):
        # 一页数量,固定20
        page_size = 20
        url = "https://sj.qq.com/myapp/cate/appList.htm?orgame=1&categoryId=0&pageSize=" + str(
            page_count * page_size) + "&pageContext=" + str((page_count + 1) * page_size)
        redis_conn = get_redis_conn(0)
        redis_conn.lpush('request_url_:1', url)


def get_url_list():
    redis_conn = get_redis_conn(0)
    return redis_conn.lrange('request_url_:1', 0, -1)


if __name__ == '__main__':
    main()
