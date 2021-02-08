from spiderHuaWei import spiderMain as HuaWei
from spiderYingYongBao import spiderMain as YingYonBao
from models import Brower
import threading
from mongoengine import connect
from e import main
from multiprocessing import Process
def run():

    tasks=[HuaWei,YingYonBao]
    for task in tasks:
        p = Process(target=task)
        p.start()


    # t = threading.Thread(target=HuaWei)
    # t.start()
    # print('开始爬取华为...')
    # t  = threading.Thread(target=YingYonBao)
    # t.start()
    # print('开始爬取应用宝')
    # t = threading.Thread(target=main)
    # t.start()



if __name__ == '__main__':
    connect("App_Data", host="127.0.0.1", port=27017)
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)',
        'User-Agent: Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+',
        'User-Agent: Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan',

    ]
    for u in user_agents:
        b = Brower(user_agent=u)
        b.save()

    run()
