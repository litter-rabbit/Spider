import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import re
import csv


'''
    程序目标：获取搜狐网国内的最新新闻板块下的前N页的所有的文章信息
    目标网站：https://news.sina.com.cn/china/
    
'''



def getcommentcounts(newsurl):  # 获取评论数


    # 使用正则获取文章id
    m = re.compile('doc-i(.*?).shtml').findall(newsurl)
    newsid = m[0]
    comments = requests.get(commenturl.format(newsid))

    # json.loads方法使字符串变为对象
    jd = json.loads(comments.text)

    # try except 是因为网络原因导致获取不到数据，会出现错误
    try:
        return jd['result']['count']['total']
    except Exception  as e:
        return 0


def get_all_news_url(url, page):
    # 保存文章url的列表
    news_url = list()
    page_url = url.format(page)
    res = requests.get(page_url).content.decode('utf-8')
    m = re.compile(r'"url":"(.*?)",').findall(res)

    # 获取的url被经过了替换，我们需要进行还原 把'\\/'还原为'/'
    for i in m:
        news_url.append(i.replace('\\/', '/'))
    return news_url


def getnewsdetail(newsurl):  # 获得单页的新闻内容

    # 保存单条新闻的内容
    result = {}
    # 使用requests库的获取内容
    res = requests.get(newsurl)
    res.encoding = 'utf-8'
    # 使用beautifulSoup解析文章内容

    soup = BeautifulSoup(res.text, 'html.parser')

    result['title'] = soup.select('.main-title')[0].text  # 标题
    timesource = soup.select('.date-source span')[0].text
    result['time'] = datetime.strptime(timesource, '%Y年%m月%d日 %H:%M').strftime('%Y-%m-%d')  # 时间
    result['place'] = soup.select('.source')[0].text  # 来源
    article = []  # 获取文章内容
    for p in soup.select('#article p')[:-1]:
        article.append(p.text.strip())
    articleall = ' '.join(article)
    result['article'] = articleall
    result['editor'] = soup.select('#article p')[-1].text.strip('责任编辑：')  # 获取作者姓名
    result['comment_num'] = getcommentcounts(newsurl)
    return result


def write_to_csv(results):

    # 指定键名
    fieldname=['title','time','place','article','editor','comment_num']
    with open('results.csv','w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=fieldname)
        # 写入第一行
        writer.writerow({'title':'标题','time':'时间','place':'来源','article':'正文','editor':'作者','comment_num':'评论数'})
        # 写入最初结果
        writer.writerows(results)





if __name__ == '__main__':



    # 获取评论的接口
    commenturl = 'http://comment5.news.sina.com.cn/page/info?version=1&format=json&channel=gn&newsid=comos-{}&group=undefined&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=3&t_size=3&h_size=3&thread=1'

    # 获取每页新闻地址的接口
    url = 'https://feed.sina.com.cn/api/roll/get?pageid=121&lid=1356&num=20&versionNumber=1.2.4&page={}&encode=utf-8&callback=feedCardJsonpCallback&_=1593076998835'

    # 用来保存的最终结果的列表
    results=list()

    # 爬取最新新闻的前十页
    for i in range(1, 10):
        print('正在获取第{}页得信息'.format(i))
        for temp_url in get_all_news_url(url, i):
            print(temp_url)
            result = getnewsdetail(temp_url)
            results.append(result)
        print('文章总数{}'.format(len(results)))
    # 写入到文件当中
    write_to_csv(results)





