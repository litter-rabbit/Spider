import requests
from lxml import etree
import csv

headers={
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'

}

#获取每页地址
def getUrl():
    results=list()
    for i in range(10):
        url = 'https://book.douban.com/top250?start={}'.format(i*25)
        result=urlData(url)
        print(result)
        results.extend(result)
    write_csv(results)



#获取每页数据
def urlData(url):
    print(url)
    html = requests.get(url,headers=headers).text

    res = etree.HTML(html)
    trs = res.xpath('//*[@id="content"]/div/div[1]/div/table/tr')
    results=list()
    for tr in trs:
        name = tr.xpath('./td[2]/div/a/text()')[0].strip()
        score = tr.xpath('./td[2]/div/span[2]/text()')[0].strip()
        comment_num = tr.xpath('./td[2]/div/span[3]/text()')[0].replace('(','').replace(')','').strip()
        info = tr.xpath('./td[2]/p[1]/text()')[0].strip()
        try:
            short_comment =tr.xpath('./td[2]/p[2]/span/text()')[0].strip()
        except Exception as e:
            short_comment=''
        info_detail = info.split('/')
        # [哥伦比亚] 加西亚·马尔克斯 / 范晔 / 南海出版公司 / 2011-6 / 39.50元
        if len(info_detail)==5:
            author=info_detail[0]
            translate_author=info_detail[1]
            publish_company= info_detail[2]
            publish_time=info_detail[3]
            price=info_detail[4]
        elif len(info_detail)==4:
            author = info_detail[0]
            translate_author = ''
            publish_company = info_detail[1]
            publish_time = info_detail[2]
            price = info_detail[3]
        else :
            author = info_detail[0]
            translate_author = ''
            publish_company = info_detail[1]
            publish_time = info_detail[2]
            price = ''

        result=dict()
        result['name']=name
        result['score']=score
        result['comment_num'] = comment_num
        result['short_comment'] =short_comment
        result['author'] = author
        result['translate_author'] = translate_author
        result['publish_company'] = publish_company
        result['publish_time'] = publish_time
        result['price'] = price
        results.append(result)

    return results








def write_csv(results):
    fieldnames = ['name', 'author', 'translate_author', 'publish_company', 'publish_time', 'price', 'score',
                  'comment_num', 'short_comment']
    with open('top_250_book.csv', 'w',newline='',encoding='gb18030') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow({'name': '书名', 'author': '作者', 'translate_author': '译者','publish_company': '出版单位', 'publish_time': '出版时间','price': '定价', 'score': '豆瓣评分', 'comment_num': '评价人数', 'short_comment': '短评'})
        writer.writerows(results)




if __name__ == '__main__':
    input('按enter键开始')
    print('正在爬取')
    getUrl()
    print('结束爬取')
    input('按enter关闭')