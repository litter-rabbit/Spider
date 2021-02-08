import requests
import re
import json
import time

def get_one_page(url):
    headers={
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }

    response = requests.get(url,headers=headers)
    if response.status_code==200:
        return response.text
    return None

def parse_one_page(html):
    pattern=re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>',re.S)
    items=re.findall(pattern,html)
    for item in items:
        yield {
            'index':item[0],
            'image':item[1],
            'title':item[2],
            'star':item[3].strip()[3:] if len(item[3])>3 else ''
        }


def write_to_file(content):
    with open('result.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False))

def change_line():
    with open('result.txt','a',) as f:
        f.write('\r\n')

def main(offset):
    url='https://maoyan.com/board/4?offset='+str(offset)
    html=get_one_page(url)
    for item in parse_one_page(html):
        write_to_file(item)
        change_line()

if __name__ == '__main__':
    for i in range(10):
        main(i*10)
        print('完成了第{}页'.format(i+1))
        time.sleep(1)








