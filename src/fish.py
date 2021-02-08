s = """
x-sgext: JAFL%2FsoBB6k%2FmGN55rMog%2F56znnMc914ynjMaMp7
umid: VF0AmLdLPA59+AJ3XN4oFpmFnWb+p+1s
x-sign: azU7Bc002xAAKAXn8GQrsMf1bl03aAXoAc40jgJK%2FiAQrdXhjpy2KOI3hc9wJedpbHBcPmoCez7G6sGcVdFB7KSspHgF%2BAXoBfgF6A
x-sid: 196fab921bc5352db109dafa8f181b9d
x-uid: 2983383209
x-nettype: WIFI
x-pv: 6.3
x-nq: WIFI
EagleEye-UserData: spm-cnt=a2170.8011571.0.0&spm-url=a2170.unknown.0.0
first_open: 0
x-features: 27
x-app-conf-v: 0
x-mini-wua: HHnB_Wvpf0MNnU%2Fu%2BMmk6L6JUQHiQV9eDFrNdI7q8bX1fGERwTxmH7bXU%2FilduRnepKvtMHc7WszfuZalkH2iYOsFIcllg81l%2FwxxUi6r8o8OGD2x3swu3xojO5aGkmyuarJf
content-type: application/x-www-form-urlencoded;charset=UTF-8
Content-Length: 788
oaid: 18052974ff1b7b8e
x-t: 1612168101
Content-Type: application/x-www-form-urlencoded;charset=UTF-8
Cookie: unb=2983383209; sn=; uc3=nk2=0vR1MffNnFyjMQ%3D%3D&vt3=F8dCuAbwIStamUI5hFY%3D&lg2=Vq8l%2BKCLz3%2F65A%3D%3D&id2=UUGq0gjFZjCTCw%3D%3D; uc1=existShop=true&cookie15=UtASsssmOIJ0bQ%3D%3D&cookie14=Uoe1gBuF8%2B7ZiQ%3D%3D&cookie21=Vq8l%2BKCLivbdjeuVIQ2NTQ%3D%3D; csg=2b0ee672; lgc=%5Cu5317%5Cu8FB0%5Cu7684%5Cu5566%5Cu5566; t=a491eb0b08e27054d04285ad1b29130c; cookie17=UUGq0gjFZjCTCw%3D%3D; sgcookie=W100q3Zlo8wkS9Rw1ChfjF5MiWRmg8rS%2BuQMxSUbztcvWfVeippxHh5WLrTrM40Pp33dz1Hl3s%2BQDfn2KvRb%2Fox%2FTyhXAFfQVuwa%2FG2%2BTPeBX%2FU%3D; dnk=%5Cu5317%5Cu8FB0%5Cu7684%5Cu5566%5Cu5566; skt=2310db91731b4f57; munb=2983383209; cookie2=196fab921bc5352db109dafa8f181b9d; uc4=nk4=0%400EUDYrYO2fjzAWBMBB47IAJB%2Bkp6&id4=0%40U2OdJhrcm1qYoNmy95DweyKekNCi; tracknick=%5Cu5317%5Cu8FB0%5Cu7684%5Cu5566%5Cu5566; _cc_=W5iHLLyFfA%3D%3D; ti=; sg=%E5%95%A695; _l_g_=Ug%3D%3D; _nk_=%5Cu5317%5Cu8FB0%5Cu7684%5Cu5566%5Cu5566; cookie1=B0SpcKk7WvAeTY%2FMhBVhK19AnSErKRvbHA0rCI%2BkSQ4%3D; _tb_token_=e535e8eeb4d4b; imewweoriw=36HCcMlV%2FnWdCtb7usW%2FhVR31Rtnnc8PJePUKnhW5fc%3D; WAPFDFDTGFG=%2B4cMKKP%2B8PI%2BuXjV2wceOuO04Q07B%2FJqsdM%3D; _w_tb_nick=%E5%8C%97%E8%BE%B0%E7%9A%84%E5%95%A6%E5%95%A6; ockeqeudmj=qarERfM%3D; isg=BE1Nm4hiETvMTbUXWBq_x_rNV2vHKoH8k8zd0Y_SiORThmw4V3pdzt6C91xFYpm0
x-bx-version: 6.5.19
f-refer: mtop
x-ttid: 231200%40fleamarket_android_6.8.90
x-app-ver: 6.8.90
x-c-traceid: YBZjQigv20YDADCiUfUNCks11612168101053004013432
x-location: 115.811435%2C27.404387
x-umt: VF0AmLdLPA59%2BAJ3XN4oFpmFnWb%2Bp%2B1s
a-orange-q: appKey=21407387&appVersion=6.8.90&clientAppIndexVersion=1120210201160701456&clientVersionIndexVersion=0
x-utdid: YBZjQigv20YDADCiUfUNCks1
x-appkey: 21407387
x-devid: AjLjrL8H0gInMEx4itYx4aqqSZDubS0VbT5ZXXlkty2V
user-agent: MTOPSDK%2F3.1.1.7+%28Android%3B10%3BXiaomi%3BMI+8+SE%29
Host: acs.m.taobao.com
Accept-Encoding: gzip
Connection: keep-alive
"""


def tojson(s):
    s = s.replace('\n', ',')

    s = s.strip()[1:-1]
    items = {k.strip(): v.strip() for k, v in [item.split(":") for item in [i for i in s.split(',')]]}

    return items

import json


def test():
    import requests
    import time

    headers = tojson(s)

    data = {"activeSearch": "false", "bizFrom": "home", "forceUseInputKeyword": "false", "forceUseTppRepair": "false",
            "fromFilter": "false", "fromKits": "false", "fromLeaf": "false", "fromShade": "false",
            "fromSuggest": "false",
            "gps": "27.404346,115.811389", "keyword": "小米解bl锁", "latitude": "27.404346", "longitude": "115.811389",
            "pageNumber": 1, "resultListLastIndex": 0, "rowsPerPage": 10,
            "searchReqFromActivatePagePart": "recommendItem",
            "searchReqFromPage": "xyHome", "searchTabType": "SEARCH_TAB_MAIN", "searchType": "common",
            "shadeBucketNum": -1, "suggestBucketNum": 28
            }

    print("headers", headers)

    print(requests.post(url="https://acs.m.taobao.com/gw/mtop.taobao.idle.search.glue/8.0/", verify=False, data=json.dumps(data),
                        headers=headers).text)


def get(x_sgext, x_umt, x_mini_wua, x_sign,timetime):
    import requests
    import time

    headers = tojson(s)
    headers['x-sgext'] = x_sgext
    headers['x-umt'] = x_umt
    headers['x-mini_wua'] = x_mini_wua
    headers['x-sign'] = x_sign
    print('接受请求时间',timetime)
    print('现在时间',str(int(time.time())))
    headers['x-t'] = timetime

    data = """{
    "data": {
        "activeSearch": false, 
        "bizFrom": "home", 
        "forceUseInputKeyword": false, 
        "forceUseTppRepair": false, 
        "fromFilter": false, 
        "fromKits": false, 
        "fromLeaf": false, 
        "fromShade": false, 
        "fromSuggest": false, 
        "gps": "27.40414,115.811719", 
        "keyword": "大江航拍无人机", 
        "latitude": "27.40414", 
        "longitude": "115.811719", 
        "pageNumber": 1, 
        "resultListLastIndex": 0, 
        "rowsPerPage": 10, 
        "searchReqFromActivatePagePart": "historyItem", 
        "searchReqFromPage": "xyHome", 
        "searchTabType": "SEARCH_TAB_MAIN", 
        "searchType": "common", 
        "shadeBucketNum": -1, 
        "suggestBucketNum": 28
    }, 
    "deviceId": "AjLjrL8H0gInMEx4itYx4aqqSZDubS0VbT5ZXXlkty2V", 
    "sid": "196fab921bc5352db109dafa8f181b9d", 
    "uid": "2983383209", 
    "x-features": "27", 
    "appKey": "21407387", 
    "api": "mtop.taobao.idle.search.glue", 
    "lat": "27.40414", 
    "lng": "115.811719", 
    "utdid": "YBZjQigv20YDADCiUfUNCks1", 
    "ttid": "231200@fleamarket_android_6.8.90", 
    "t": "%s", 
    "v": "8.0"
}"""%timetime

    print("headers", headers)
    print("data",data)
    session = requests.session()
    res = session.request(method='post',url="https://acs.m.taobao.com/gw/mtop.taobao.idle.search.glue/8.0/",data=json.loads(data),headers=headers,verify=False)
    print(res.text)




if __name__ == '__main__':
    import time

    s="%7B%22"
    from urllib import parse
    #res = parse.unquote("data=%7B%22activeSearch%22%3Afalse%2C%22bizFrom%22%3A%22hom%22%2C%22forceUseInputKeyword%22%3Afalse%2C%22forceUseTppRepair%22%3Afalse%2C%22fromFilter%22%3Afalse%2C%22fromKits%22%3Afalse%2C%22fromLeaf%22%3Afalse%2C%22fromShade%22%3Afalse%2C%22fromSuggest%22%3Afalse%2C%22gps%22%3A%2227.404286%2C115.811381%22%2C%22keyword%22%3A%22%E5%8D%8E%E4%B8%BAnexus6p%22%2C%22latitude%22%3A%2227.404286%22%2C%22longitude%22%3A%22115.811381%22%2C%22pageNumber%22%3A1%2C%22resultListLastIndex%22%3A0%2C%22rowsPerPage%22%3A10%2C%22searchReqFromActivatePagePart%22%3A%22historyItem%22%2C%22searchReqFromPage%22%3A%22xyHome%22%2C%22searchTabType%22%3A%22SEARCH_TAB_MAIN%22%2C%22searchType%22%3A%22common%22%2C%22shadeBucketNum%22%3A-1%2C%22suggestBucketNum%22%3A28%7D")
    res = parse.quote('{"activeSearch":false,"bizFrom":"hom","forceUseInputKeyword":false,"forceUseTppRepair":false,"fromFilter":false,"fromKits":false,"fromLeaf":false,"fromShade":false,"fromSuggest":false,"gps":"27.404286,115.811381","keyword":"华为nexus6p","latitude":"27.404286","longitude":"115.811381","pageNumber":1,"resultListLastIndex":0,"rowsPerPage":10,"searchReqFromActivatePagePart":"historyItem","searchReqFromPage":"xyHome","searchTabType":"SEARCH_TAB_MAIN","searchType":"common","shadeBucketNum":-1,"suggestBucketNum":28}')

    print(res)

#=%7B%22activeSearch%22%3Afalse%2%22bizFrom%22%3A%22home%22%2C%22forceUseInputKeyword%22%3Afalse%2C%22forceUseTppRepair%22%3Afalse%2C%22fromFilter%22%3Afalse%2C%22fromKits%22%3Afalse%2C%22fromLeaf%22%3Afalse%2C%22fromShade%22%3Afalse%2C%22fromSuggest%22%3Afalse%2C%22gps%22%3A%2227.404424%2C115.811475%22%2C%22keyword%22%3A%22%E5%8D%8E%E4%B8%BAnexus6p%22%2C%22latitude%22%3A%2227.404424%22%2C%22longitude%22%3A%22115.811475%22%2C%22pageNumber%22%3A1%2C%22resultListLastIndex%22%3A0%2C%22rowsPerPage%22%3A10%2C%22searchReqFromActivatePagePart%22%3A%22historyItem%22%2C%22searchReqFromPage%22%3A%22xyHome%22%2C%22searchTabType%22%3A%22SEARCH_TAB_MAIN%22%2C%22searchType%22%3A%22common%22%2C%22shadeBucketNum%22%3A-1%2C%22suggestBucketNum%22%3A28%7D"
    "%7B%22activeSearch%22%3Afalse%2C%22bizFrom%22%3A%22home%22%2C%22forceUseInputKeyword%22%3Afalse%2C%22forceUseTppRepair%22%3Afalse%2C%22fromFilter%22%3Afalse%2C%22fromKits%22%3Afalse%2C%22fromLeaf%22%3Afalse%2C%22fromShade%22%3Afalse%2C%22fromSuggest%22%3Afalse%2C%22gps%22%3A%2227.404425%2C115.811476%22%2C%22keyword%22%3A%22%E5%B0%8F%E7%B1%B3%E8%A7%A3bl%E9%94%81%22%2C%22latitude%22%3A%2227.404425%22%2C%22longitude%22%3A%22115.811476%22%2C%22pageNumber%22%3A1%2C%22resultListLastIndex%22%3A0%2C%22rowsPerPage%22%3A10%2C%22searchReqFromActivatePagePart%22%3A%22historyItem%22%2C%22searchReqFromPage%22%3A%22xyHome%22%2C%22searchTabType%22%3A%22SEARCH_TAB_MAIN%22%2C%22searchType%22%3A%22common%22%2C%22shadeBucketNum%22%3A-1%2C%22suggestBucketNum%22%3A28%7D"