from app_spider.HuaWei import main as HuaWei
from app_spider.YingYongBao import main as YingYongBao

import threading
def run():
    task = threading.Thread(target=HuaWei)
    task.start()
    task = threading.Thread(target=YingYongBao)
    task.start()


if __name__ == '__main__':
    run()






