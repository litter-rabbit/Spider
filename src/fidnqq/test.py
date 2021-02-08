# from urllib import request as urlrequest
# import json
# name='474213358'
# req = urlrequest.Request(url='http://test.anyou99.com/get_qqinfo?qq={}'.format(name))
# res = urlrequest.urlopen(req)
# res = res.read().decode('utf-8')
# res = json.loads(res)
# status = res['status']
# # '{"status":"1","data":[["416114288","湖南大学二手群","2020-10-27T11:34:12"]]}'
# if status:
#     res = res['data']
#     res=json.loads(res)
#     print(res)
#     if res['errcode']==0:
#         active=res['group_list'][0]['activity']
#         qq=res['group_list'][0]['code']
#         group_label_list=res['group_list'][0]['group_label']
#         try:
#             label_list=res['group_list'][0]['labels']
#         except Exception as e:
#             label_list = ''
#         name=res['group_list'][0]['name']
#         logo=res['group_list'][0]['url']
#         info_list=res['group_list'][0]['gcate']
#         print(active)
#         print(qq)
#         print(group_label_list)
#         print(label_list)
#         print(name)
#         print(logo)
#         print(info_list)


def test():
    cookei='uin = o0709343607;skey =@AqZoaGshg'
    from urllib import parse
    cookie=parse.quote(cookei)
    print(cookie)
    cookie=parse.unquote(cookie)
    print(cookie)

if __name__ == '__main__':
    test()


