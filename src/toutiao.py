import requests
from urllib.parse import urlencode
import os
from hashlib import md5


def get_page(offset):
    params={
        'aid': '24',
        'app_name': 'web_search',
        'offset': offset,
        'format': 'json',
        'keyword': '街拍',
        'autoload': 'true',
        'count': '20',
        'en_qc': '1',
        'cur_tab': '1',
        'from': 'search_tab',
        'pd': 'synthesis',
    }

    headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'referer': 'https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D',
        'x-requested-with': 'XMLHttpRequest',
        'cookie': 'tt_webid=6794251315515115021; s_v_web_id=k6pwbhq9_NacZWSGp_WVYt_4Q1l_950f_kt9BTR3jRrV1; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6794251315515115021; csrftoken=19994eee79496d0914ac549fda782033; ttcid=62258c9535b043028d220de7bb5c55a933; __tasessionId=tpyn3rwen1581915598534; tt_scid=qsAAIBlVnw0-XGjA-GgTEVNTwjTf4h8J3oLH9P77M3AdtV2Uvvun8lJV3-8bOdW618c3'
    }

    url='https://www.toutiao.com/api/search/content/?'+urlencode(params)
    try:
        response=requests.get(url,headers=headers)
        if response.status_code==200:
            return response.json()
    except requests.ConnectionError as e:
        print("Error",e.args)
        return None

def get_image(json):
    if json.get('data'):
        for item in json.get('data'):
            title=item.get('title')
            images=item.get('image_list')
            for image in images:
                yield {
                    'image':image.get('url'),
                    'title':title
                }

def save_image(item):

    if not os.path.exists(item.get('title')):
        os.mkdir(item.get('title'))
    try:
        response = requests.get(item.get('image'))
        if response.status_code==200:
            file_path='{0}/{1}.{2}'.format(item.get('title'),md5(response.content).hexdigest(),'jpg')
            if not os.path.exists(file_path):
                with open(file_path,'wb') as f:
                    f.write(response.content)
                    print('完成下载')
            else:
                print("Already has Download")
    except requests.ConnectionError as e:
        print("Error",e.args)



def main(offset):
    json=get_page(offset)
    for item in get_image(json):
        save_image(item)
        print(item)

GROUND_START=1
GROUND_END=3

if __name__ == '__main__':

    from multiprocessing.pool import Pool
    pool=Pool()
    groups=[x*20 for x in range(GROUND_START,GROUND_END+1)]
    pool.map(main,groups)
    pool.close()
    pool.join()












