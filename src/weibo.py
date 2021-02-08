from urllib.parse import urlencode
from pyquery import PyQuery as pq
import requests


headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',

    'Referer': 'https://m.weibo.cn/u/2830678474',
    'X-Requested-With': 'XMLHttpRequest',
    'Accept': 'application/json, text/plain, */*',
    'MWeibo-Pwa': '1'
}


base_url='https://m.weibo.cn/api/container/getIndex?'

def get_page(page):
    params={
        'type':'uid',
        'value':'2830678474',
        'containerid':'1076032830678474',
        'since_id':page

    }

    url=base_url+urlencode(params)
    try:
        response = requests.get(url,headers=headers)
        if response.status_code==200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error',e.args)


def parse_page(json):
    if json:
        items = json.get('data').get('cards')
        for item in items:
            item=item.get('mblog')
            weibo={}
            weibo['id']=item.get('id')
            weibo['text']=pq(item.get('text')).text()
            yield weibo


if __name__ == '__main__':
    sinid_id=4469643543009070
    json=get_page(sinid_id)
    results=parse_page(json)
    for result in results:
        print(result)




