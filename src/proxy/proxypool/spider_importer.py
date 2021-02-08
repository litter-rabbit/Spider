from proxypool.redis_db import RedisClient

conn = RedisClient()

"""
 可以进行手动录入代理，
"""

def set_proxy(proxy):
    result = conn.add(proxy)
    print(proxy)
    print('录入成功' if result else '录入失败')



"""
 查询redis是否有输入的代理
"""

def scan_proxy():
    print('请输入代理, 输入exit退出读入')
    while True:
        proxy = input()
        if proxy == 'exit':
            break
        set_proxy(proxy)


if __name__ == '__main__':
    scan_proxy()
