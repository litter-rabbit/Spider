import requests
from bs4 import BeautifulSoup
import re

url='https://www.qiushibaike.com/8hr/page/1/'


def crawl():

    r=requests.get(url).text
    pattern_author = re.compile(u'<span class="recmd-name">(.*?)</span>', re.S)
    pattern_funnum = re.compile('<div class="recmd-num">[\n]*<span>(.*?)</span>',re.S)
    pattern_comment = re.compile('<span>.</span>[\n]*<span>(.*?)</span>',re.S)

    soup = BeautifulSoup(r,'lxml')
    span=soup.select('.recmd-num')
    comment=list()
    fun=list()
    for i in span:
        if len(i.contents)==9:
            fun.append(i.contents[2].text)
            comment.append(i.contents[6])



    def wordcloud():
        import jieba
        from wordcloud import WordCloud
        import matplotlib.pyplot as plt
        text = ''
        with open('results.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                text += row['正文']
        words = jieba.lcut(text)

        cuted = ' '.join(words)

        fontpath = '江城圆体 700W.ttf'
        wc = WordCloud(font_path=fontpath,  # 设置字体
                       background_color="white",  # 背景颜色
                       max_words=1000,  # 词云显示的最大词数
                       max_font_size=500,  # 字体最大值
                       min_font_size=20,  # 字体最小值
                       random_state=42,  # 随机数
                       collocations=False,  # 避免重复单词
                       width=1600, height=1200, margin=10,
                       )
        wc.generate(cuted)

        plt.figure(dpi=100)  # 通过这里可以放大或缩小
        plt.imshow(wc, interpolation='catrom', vmax=1000)
        plt.axis("off")  # 隐藏坐标
        plt.show()









