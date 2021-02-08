from utils import header2json, save_response
from tornado import queues
import time
from tornado import gen
import aiohttp
import re
import parsel

base_url = "https://api.zhihu.com/search_v3?correction=1&t=general&q={}"
header_str = """
authority: api.zhihu.com
scheme: https
x-api-version: 3.0.65
user-agent: com.zhihu.android/Futureve/5.6.2 Mozilla/5.0 (Linux; Android 10; MI 8 SE Build/QKQ1.190828.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.101 Mobile Safari/537.36
x-app-version: 5.6.2
x-app-za: OS=Android&Release=10&Model=MI+8+SE&VersionName=5.6.2&VersionCode=575&Width=1080&Height=2115&Installer=xiaomi-preinstall&WebView=83.0.4103.101DeviceType=AndroidPhoneBrand=Xiaomi
x-app-flavor: xiaomi-preinstall
x-app-build: release
x-network-type: WiFi
x-suger: QU5EUk9JRF9JRD00MmZhNmJjZjQwNTJkYTVkO01BQz0wMjowMDowMDowMDowMDowMA==
x-udid: AECfdPcTkhJLBULRdqBjxqlATYNw3yOAeLw=
authorization: Bearer gt2.0AAAAACoG5T4SkhP3dJ9AAAAAAAxNVQJgAgBGe5JmXd1W_QEsoso9wQSr7qGMEg==
cookie: q_c1=5faaf4e0868f4d9298bdb87eee51f210|1612358076000|1612358076000; z_c0=2|1:0|10:1612358075|4:z_c0|92:Z3QyLjBBQUFBQUNvRzVUNFNraFAzZEo5QUFBQUFBQXhOVlFKZ0FnQkdlNUptWGQxV19RRXNvc285d1FTcjdxR01FZz09|36e4e1997aab7ededeb8a7ff270341919e95137728d7328b893a8b0ab37a205d; KLBRSID=b33d76655747159914ef8c32323d16fd|1612358604|1612358075; _xsrf=bbglFNjIyPkZB9NKl4HO3D470Axl863m
accept-encoding: gzip
"""


# authorization: Bearer gt2.0AAAAACoG5T4SkhP3dJ9AAAAAAAxNVQJgAgBGe5JmXd1W_QEsoso9wQSr7qGMEg==

def print_exception_info(url, e, rsp=None):
    print('解析数据出错{}:{}:{}'.format(url, e, str(rsp)[:70]))
    dead.add(url)


async def get_json_from_url(url, method='get', data=None):
    async with  aiohttp.ClientSession() as session:
        if method == 'get':
            try:
                response = await session.get(url=url, headers=headers)
            except Exception as e:
                print('请求出错{}:{}'.format(url, str(e)))
                return None
        elif method == 'post':
            try:
                response = await session.post(url=url, headers=headers, data=data)
            except Exception as e:
                print('请求出错{}:{}'.format(url, str(e)))
                return None
        return await response.json()


async def get_html_from_url(url, method='get', data=None):
    async with aiohttp.ClientSession() as session:
        if method == 'get':
            try:
                response = await session.get(url=url, headers=headers)
            except Exception as e:
                print('请求出错{}:{}'.format(url, str(e)))
                return None
        elif method == 'post':
            try:
                response = await session.post(url=url, headers=headers, data=data)
            except Exception as e:
                print('请求出错{}:{}'.format(url, str(e)))
                return None
        return await response.text(encoding='utf8')


async def get_search_url(search_url):
    rsp_json = await get_json_from_url(search_url)
    if not rsp_json:
        return
    try:
        if rsp_json['paging']['is_end'] == 'false' or rsp_json['paging']['is_end'] is False:
            next_search_url = rsp_json['paging'].get('next')
            await q.put(next_search_url)
    except Exception as e:
        print_exception_info(search_url, e, rsp_json)
        return

    try:
        for question in rsp_json['data'][1:]:
            try:
                await q.put(question['object']['question']['url'])
            except Exception as e:
                print('1')
                pass
    except Exception as e:
        print_exception_info(search_url, e, rsp_json)


async def get_answer_batch_url(question_url):
    rsp_json = await get_json_from_url(question_url)
    if not rsp_json:
        return
    try:
        anwser_count = int(rsp_json['answer_count'])
        if str(question_url).endswith('/'):
            anwer_base_url = question_url + "answers?order_by=&offset={}"
        else:
            anwer_base_url = question_url + "/answers?order_by=&offset={}"
        for i in range(1, int(anwser_count / 5)):
            await q.put(anwer_base_url.format(i * 5))
    except Exception as e:
        print_exception_info(question_url, e, rsp_json)


async def get_answer_url(answer_batch_url):
    rsp_json = await get_json_from_url(answer_batch_url)
    if not rsp_json:
        return
    try:
        for anwser in rsp_json['data']:
            answer_base_urt = "https://www.zhihu.com/appview/answer/{}?appview=1&config=%7B%22content_padding_top%22%3A144%2C%22content_padding_bottom%22%3A56%2C%22content_padding_left%22%3A16%2C%22content_padding_right%22%3A16%2C%22title_font_size%22%3A22%2C%22body_font_size%22%3A16%2C%22is_dark_theme%22%3Afalse%2C%22can_auto_load_image%22%3Atrue%2C%22app_info%22%3A%22OS%3DAndroid%26Release%3D10%26Model%3DMI%2B8%2BSE%26VersionName%3D5.6.2%26VersionCode%3D575%26Width%3D1080%26Height%3D2115%26Installer%3Dxiaomi-preinstall%26WebView%3D83.0.4103.101DeviceType%3DAndroidPhoneBrand%3DXiaomi%22%2C%22X-SUGER%22%3A%22QU5EUk9JRF9JRD00MmZhNmJjZjQwNTJkYTVkO01BQz0wMjowMDowMDowMDowMDowMA%3D%3D%22%7D&type=0"
            await q.put(answer_base_urt.format(anwser['id']))
    except Exception as e:
        print_exception_info(answer_batch_url, e, rsp_json)


async def get_answer_data(answer_url):
    rsp_text = await get_html_from_url(answer_url)
    if not rsp_text:
        return
    html = parsel.Selector(rsp_text)
    text_list = html.css('".RichText p::text"').extract()
    text = '\n'.join(text_list)


async def deal_url(url):
    if url in feting:
        return
    feting.add(url)
    print('正在处理{}'.format(url))
    if "search_v3" in url:
        print('搜索url地址')
        await get_search_url(url)
    elif re.match(r"^https://api.zhihu.com/questions/\d+[0-9/]$", url):
        print('问题url地址')
        await get_answer_batch_url(url)
    elif re.match(r"^https://api.zhihu.com/questions/\d+/answers\?order_by=&offset=\d+[0-9/]$",
                  url):
        print('batch回答url')
        await get_answer_url(url)
    elif "appview" in url:
        print('回答url地址')
        await get_answer_data(url)
    print('处理完成{}'.format(url))
    feted.add(url)


async def main():
    async def worker():
        async for url in q:
            if url is None:
                return
            try:
                await deal_url(url)
            except Exception as e:
                print('Exception :{}', str(e))
                dead.append(url)

    for i in search_word:
        await q.put(base_url.format(i))
    workers = gen.multi([worker() for _ in range(max_workers_num)])
    from datetime import timedelta
    await q.join(timeout=timedelta(seconds=60))
    print('共获取urls数量为: {}'.format(len(feted)))
    print('失败数量为:{}'.format(len(dead)))
    print('抓取用时{}'.format(time.time() - start))
    for _ in range(max_workers_num):
        await q.put(None)
    await workers


async def test():
    rsp = await  get_html_from_url(
        url="https://www.zhihu.com/appview/answer/927792157?appview=1&config=%7B%22content_padding_top%22%3A144%2C%22content_padding_bottom%22%3A56%2C%22content_padding_left%22%3A16%2C%22content_padding_right%22%3A16%2C%22title_font_size%22%3A22%2C%22body_font_size%22%3A16%2C%22is_dark_theme%22%3Afalse%2C%22can_auto_load_image%22%3Atrue%2C%22app_info%22%3A%22OS%3DAndroid%26Release%3D10%26Model%3DMI%2B8%2BSE%26VersionName%3D5.6.2%26VersionCode%3D575%26Width%3D1080%26Height%3D2115%26Installer%3Dxiaomi-preinstall%26WebView%3D83.0.4103.101DeviceType%3DAndroidPhoneBrand%3DXiaomi%22%2C%22X-SUGER%22%3A%22QU5EUk9JRF9JRD00MmZhNmJjZjQwNTJkYTVkO01BQz0wMjowMDowMDowMDowMDowMA%3D%3D%22%7D&type=0")
    html = parsel.Selector(rsp)
    text = html.css(".RichText p::text").extract()

    print(text)






if __name__ == '__main__':
    import tornado.ioloop

    q = queues.Queue()
    start = time.time()
    search_word = ['零食']
    max_workers_num = 50
    feting, feted, dead = set(), set(), set()
    headers = header2json(header_str)
    ioloop = tornado.ioloop.IOLoop().current()
    ioloop.run_sync(main)
    # ioloop.run_sync(test)
