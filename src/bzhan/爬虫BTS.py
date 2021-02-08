# 1.导入我们要用到的模块
import requests  # 引入requests模块，用于访问网络数据
import json  # 引入json模块，用于处理json数据
import chardet  # 引入chardet模块，用于识别编码
import re  # 引入re模块，用于进行正则表达式判断
from pprint import pprint  # 用于打印一系列的信息


# 2.根据bvid请求得到cid
def get_cid():  # 定义get_cid函数
    url = 'https://api.bilibili.com/x/player/pagelist?bvid=BV1D7411w7z6&jsonp=jsonp'  # 获取cid的视频接口地址
    res = requests.get(url).text  # 获取HTML网页的内容
    json_dict = json.loads(res)  # 从网页内容中将其转化成json数据
    # pprint(json_dict)            #批量化输出字典内容
    return json_dict["data"][0]["cid"]  # 将字典内容里的cid返回


# 3.根据cid请求弹幕，解析弹幕得到最终的数据
def get_data(cid):
    final_url = "https://api.bilibili.com/x/v1/dm/list.so?oid=" + str(154821195)
    final_res = requests.get(final_url)
    final_res.encoding = chardet.detect(final_res.content)['encoding']
    final_res = final_res.text
    pattern = re.compile('<d.*?>(.*?)</d>')
    data = pattern.findall(final_res)
    # pprint(final_res)
    return data


# 4.保存弹幕列表
def save_to_file(data):
    with open("BTS_danmu.txt", mode="w", encoding="utf-8") as f:
        for i in data:
            f.write(i)
            f.write("\n")


# 5.生成词云图片
def generate_wordcloud():

    # 获取数据保存成一个字符串
    text = ''
    with open('BTS_danmu.txt', mode='r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            text += line

    import jieba
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt

    # 对字符串进行分割 ，比如：今天吃饭了没 分割为 今天 吃饭 了 没
    words = jieba.lcut(text)

    # 使用 ' '进行连接成一个字符串
    cuted = ' '.join(words)

    # 字体
    fontpath = '江城圆体 700W.ttf'

    # 生成词云
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

    # 显示图片
    plt.figure(dpi=100)  # 通过这里可以放大或缩小
    plt.imshow(wc, interpolation='catrom', vmax=1000)
    plt.axis("off")  # 隐藏坐标
    plt.show()


cid = get_cid()
data = get_data(cid)
save_to_file(data)
generate_wordcloud()
