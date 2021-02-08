


import requests


def get(url):

    response=requests.request('GET',url)
    print(response.text)


if __name__ == '__main__':
    url='http://www.lrabbit.life/category/3'
    get(url)

