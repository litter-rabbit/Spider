import asyncio
import aiohttp
import time
import sys

try:
    from aiohttp import ClientError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError
from proxypool.redis_db import RedisClient
from proxypool.spider_setting import *


class SpiderTester(object):
    def __init__(self):
        self.redis = RedisClient()

    async def test_single_proxy(self, proxy):

        """"""
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                print('正在测试', proxy)
                async with session.get(TEST_URL, proxy=real_proxy, timeout=15, allow_redirects=False) as response:
                    if response.status in VALID_STATUS_CODES:

                        # 如果代码可以用就将这个ip的分数设置为最大
                        self.redis.max(proxy)
                        print('代理可用', proxy)
                    else:
                        # 如果这个ip不可以用，就将这个ip的分数减5分
                        self.redis.decrease(proxy)
                        print('请求响应码不合法 ', response.status, 'IP', proxy)
            except (ClientError, aiohttp.client_exceptions.ClientConnectorError, asyncio.TimeoutError, AttributeError):
                self.redis.decrease(proxy)
                print('代理请求失败', proxy)

    """遍历redis中的ip,进行测试"""
    def run(self):

        print('测试器开始运行')
        try:
            count = self.redis.count()
            print('当前剩余', count, '个代理')
            for i in range(0, count, BATCH_TEST_SIZE):
                start = i
                stop = min(i + BATCH_TEST_SIZE, count)
                print('正在测试第', start + 1, '-', stop, '个代理')
                test_proxies = self.redis.batch(start, stop)

                """使用异步的方式测试ip"""
                loop = asyncio.get_event_loop()
                # 将所有需要测试的ip任务放入到一个列表中
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]

                loop.run_until_complete(asyncio.wait(tasks))
                sys.stdout.flush()
                time.sleep(5)
        except Exception as e:
            print('测试器发生错误', e.args)
