from proxypool.spider_tester import SpiderTester

from proxypool.redis_db import RedisClient
from proxypool.spider import Spider
from proxypool.spider_setting import *
import sys



class Spider_getter():
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Spider()

    def is_over_threshold(self):
        """
        判断是否达到了代理池限制
        """
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False


    """
        调用爬虫类里面的爬取网站函数，进行爬取，将爬取的结果放入redis中
    """
    def begin(self):
        print('获取器开始执行')
        if not self.is_over_threshold():
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[callback_label]
                # 获取代理
                proxies = self.crawler.get_proxies(callback)
                sys.stdout.flush()
                for proxy in proxies:
                    self.redis.add(proxy)
