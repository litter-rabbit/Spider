
from proxypool.spider_scheduler import SpiderScheduler

import sys
import io

"""主函数"""

sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

def start_work():
    try:
        s=SpiderScheduler()
        s.start()
    except:
        start_work()

if __name__ == '__main__':
    start_work()
