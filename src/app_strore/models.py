import random

from mongoengine import *

# connect("App_Data", host="10.13.88.111", port=27017)
connect("App_Data", host="127.0.0.1", port=27017)


class Appdata(Document):
    app_id = StringField(max_length=32, primary_key=True)
    app_store = StringField(max_length=3, verbose_name="应用商店")
    app_name = StringField(max_length=255, verbose_name="应用名称")
    description = StringField(max_length=20000, verbose_name="简介")
    app_down_count = StringField(max_length=255, verbose_name="下载量")
    average_rating = DecimalField(max_digits=32, decimal_places=16, verbose_name="评分")
    category_name = StringField(max_length=255, verbose_name="分类")


class Brower(Document):
    user_agent = StringField(max_length=255, verbose_name="user-agent")
    info = StringField(max_length=255, blank=True, null=True, verbose_name="附加信息")
    useful = StringField(max_length=1, default="1", verbose_name="是否可用(1:可用, 0,不可用)")


class Proxy(Document):
    ip = StringField(max_length=255, verbose_name="服务器ip")
    http_type = StringField(max_length=10, verbose_name="服务器端口")
    port = IntField(verbose_name="服务器端口")
    useful = StringField(max_length=1, default="1", verbose_name="是否可用")
    meta = {'collection': 'proxy'}


class Comment(Document):
    comment_id = StringField(max_length=255, verbose_name="评论id")
    comment_info = StringField(max_length=3000, verbose_name="评论具体内容")
    stars = StringField(max_length=2, verbose_name="该评论星星数")
    app_store = StringField(max_length=255, verbose_name="所在应用商店")
    app_id = StringField(max_length=255, verbose_name="该评论针对的app")


if __name__ == '__main__':
    b = Brower(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',info='useraget',useful='1')
    b.save()