import time
from multiprocessing import Process
from proxypool.spider_api import app
from proxypool.get_proxy import Spider_getter
from proxypool.spider_tester import SpiderTester
from proxypool.redis_db import RedisClient
from proxypool.spider_setting import *

"""
调度器类
"""

class SpiderScheduler():

    """
        测试代理，不合格的代理进行减分

    """
    def spider_tester(self, cycle=TESTER_CYCLE):
        """
        定时测试代理
        """
        tester = SpiderTester()
        while True:
            print('测试器开始运行')
            tester.run()
            time.sleep(cycle)

    """每个一段时间运行抓取函数"""

    def schedule_getter(self, cycle=GETTER_CYCLE):
        """
        定时获取代理
        """
        getter = Spider_getter()
        while True:
            print('开始抓取代理')
            getter.begin()
            time.sleep(cycle)

    """开启flask的api,这个可以通过访问127.0.0.1：5000/random获取一个随机代理"""

    def schedule_api(self):
        """
        开启API
        """
        app.run(API_HOST, API_PORT)



    def start(self):
        print('代理池开始运行')

        """开启一个新的进程运行测试函数"""
        if TESTER_ENABLED:
            tester_process = Process(target=self.spider_tester)
            tester_process.start()

        """同理"""
        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()

        if API_ENABLED:
            api_process = Process(target=self.schedule_api)
            api_process.start()
