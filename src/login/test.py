

from DecryptLogin import login


class Crawl:

    @staticmethod
    def login():
        lg=login.Login()
        infos,session=lg.taobao()
        return session


if __name__ == '__main__':
    print()
