import json
import pymongo


client = pymongo.MongoClient(host='127.0.0.1',port=27017)

zhihu = client['zhihu']['response']



def header2json(s):
    s = s.split('\n')
    s = filter(lambda x: len(x) > 0, s)

    return {item.split(':')[0]: item.split(':')[1] for item in s}


def save_response(url,response):

    zhihu.insert({url:url,response:response})
