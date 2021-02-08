import random


from django.utils.html import format_html

from mongoengine import *
connect("App_Data",host="10.13.88.111",port=27017)
class Appdata(Document):
    app_id = StringField(max_length=32, primary_key=True)
    app_store = StringField(max_length=3, verbose_name="应用商店")
    app_name = StringField(max_length=255, verbose_name="应用名称")
    description = StringField(max_length=20000,verbose_name="简介")
    app_down_count = StringField(max_length=255, verbose_name="下载量")
    average_rating = DecimalField(max_digits=32, decimal_places=16, verbose_name="评分")
    category_name = StringField(max_length=255, verbose_name="分类")

    def __str__(self):
        return format_html("["+str(self.app_id) + "|" +str(self.app_store) + "&nbsp;&nbsp;|&nbsp;&nbsp;" + str(self.app_name) + "&nbsp;|&nbsp;下载量:" + str(
            self.app_down_count) + "&nbsp;|&nbsp;评分:" + str(self.average_rating) + " ]")


    class Meta:
        managed = False
        db_table = 'appdata'
        unique_together = (('app_id', 'app_store'),)
        verbose_name = u"03-爬取的应用数据 (appdata)"  # 单数形式
        verbose_name_plural = verbose_name  # 复数形式



class Brower(Document):
    user_agent = StringField(max_length=255, verbose_name="user-agent")
    info = StringField(max_length=255, blank=True, null=True, verbose_name="附加信息")
    useful = StringField(max_length=1, default="1", verbose_name="是否可用(1:可用, 0,不可用)")

    def __str__(self):
        return "[" + str(self.id) + "__|__" + str(self.info) + " ]"

    class Meta:
        managed = False
        db_table = 'brower'
        verbose_name = u"02-浏览器 (brower)"  # 单数形式
        verbose_name_plural = verbose_name  # 复数形式

class Proxy(Document):
    ip = StringField(max_length=255, verbose_name="服务器ip")
    http_type = StringField(max_length=10, verbose_name="服务器端口")
    port = IntField(verbose_name="服务器端口")
    useful = StringField(max_length=1, default="1", verbose_name="是否可用")
    meta = {'collection': 'proxy'}
    def __str__(self):
        return "[" + str(self.ip) + ":" + str(self.port) + "__|__" + str(self.useful) + " ]"

    class Meta:
        managed = False
        db_table = 'proxy'
        unique_together = (('ip', 'port'),)
        verbose_name = u"01-爬虫代理 (proxy)"  # 单数形式
        verbose_name_plural = verbose_name  # 复数形式


class Comment(Document):
    comment_id = StringField(max_length=255,verbose_name="评论id")
    comment_info = StringField(max_length=3000,verbose_name="评论具体内容")
    stars = StringField(max_length=2,verbose_name="该评论星星数")
    app_store = StringField(max_length=255,verbose_name="所在应用商店")
    app_id = StringField(max_length=255,verbose_name="该评论针对的app")
    def __str__(self):
        return "["+str(self.app_store) + "|appId:"+str(self.app_id) + "|星星数:"+str(self.stars) + "|评论id:"+str(self.comment_id) + "|"+ "|"+str(self.comment_info) + "]"
    class Meta:
        managed = False
        db_table = 'comment'
        verbose_name = u"05-关于app的评论 (comment)"  # 单数形式
        verbose_name_plural = verbose_name  # 复数形式
        unique_together = (('comment_id', 'app_store'),)


