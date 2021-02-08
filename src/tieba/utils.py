import pymysql

import requests
import json

Cookie = "JSESSIONID=BAAE61D4FBECC955F6E7E42CAB1AA76B"
headers = {
    "Content-Type": "application/json",
    "Origin": "http://kd.nsfc.gov.cn",
    "Cookie": Cookie,
    "Origin": "http://kd.nsfc.gov.cn",
    "Referer": "http://kd.nsfc.gov.cn/baseQuery/conclusionQuery",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
}

data = {
    "adminID": "",
    "beginYear": "",
    "checkDep": "",
    "checkType": "",
    "code": "",
    "complete": "true",
    "conclusionYear": "",
    "dependUnit": "",
    "endYear": "",
    "keywords": "",
    "pageNum": 0,
    "pageSize": 50,
    "personInCharge": "",
    "projectName": "",
    "projectType": "",
    "psPType": "",
    "queryType": "input",
    "quickQueryInput": "",
    "ratifyNo": "",
    "ratifyYear": "",
    "subPType": "",
    "type": ""
}

person_data = {
    "adminID": "",
    "beginYear": "",
    "checkDep": "",
    "checkType": "",
    "code": "",
    "complete": "true",
    "conclusionYear": "",
    "dependUnit": "",
    "endYear": "",
    "id": "",
    "keywords": "",
    "pageNum": 0,
    "pageSize": 50,
    "personInCharge": "",
    "projectName": "",
    "projectType": "",
    "psPType": "",
    "queryType": "input",
    "quickQueryInput": "",
    "ratifyNo": "",
    "ratifyYear": "",
    "subPType": "",
    "type": "person"
}


def get_db():
    return pymysql.connect(host='127.0.0.1', user='root', password='123456', database='sci', charset='utf8mb4')

def get_db1():
    return pymysql.connect(host='127.0.0.1', user='root', password='123456', database='sci', charset='utf8mb4')


def insert_project(*args, **kwargs):
    db = get_db1()
    conn = db.cursor()
    if args[0] == 'project':
        sql = "insert into project(`number`,`position`,`study_duration`,`study_result`,`admin_id`," \
              "`title`,`group`,`catetory`,`money`,`master`,`company`,`year`) value ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(

            kwargs['number'], kwargs['position'], kwargs['study_duration'], kwargs['study_result'], kwargs['admin_id'],
            kwargs['title'], kwargs['group'], kwargs['catetory'], kwargs['money'], kwargs['master'],kwargs['company'],
            kwargs['year']
        )
        sql_exeist = "select count(id) from project where number='{}'".format(kwargs['number'])

        print(sql_exeist)
        conn.execute(sql_exeist)
        res = conn.fetchall()
        print(res)
        if res[0][0] > 0:
            print('已经存在')
            return
        try:
            conn.execute(sql)
            db.commit()
            print('插入成功项目')
        except Exception as e:
            db.rollback()
            print(str(e))
            print('失败',sql)
    elif args[0] == 'part_person':
        sql_exist = "select count(id) from part_person where `number_key`='{}' and `name`='{}'".format(kwargs['number_key'],
                                                                                                  kwargs['name'])
        print(sql_exist)
        conn.execute(sql_exist)
        res = conn.fetchall()
        if res[0][0] > 0:
            print('已经存在')
            return
        sql = "insert into part_person(`name`,`position`,`company`,`number_key`,`person_id`) value('{}','{}','{}','{}','{}')".format(

            kwargs['name'], kwargs['position'], kwargs['company'], kwargs['number_key'], kwargs['person_id']
        )
        print(sql)
        try:
            conn.execute(sql)
            db.commit()
            print('插入项目参与人',kwargs['name'])
        except Exception as e:
            db.rollback()
            print('失败',sql)

    elif args[0]=='rela_project':
        sql_exist = "select count(id) from rela_project where `number_key`='{}' and `number`='{}'".format(kwargs['number_key'],kwargs['number'])
        print(sql_exist)
        conn.execute(sql_exist)
        res = conn.fetchall()
        if res[0][0] > 0:
            print('已经存在')
            return
        sql = "insert into rela_project(`title`,`number`,`year`,`catetory`,`money`,`master`,`company`,`number_key`,`is_master`) value('{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
            kwargs['title'],kwargs['number'],kwargs['year'],kwargs['catetory'],kwargs['money'],kwargs['master'],kwargs['company'],
            kwargs['number_key'],kwargs['is_master']
        )
        print(sql)
        try:
            conn.execute(sql)
            db.commit()
            print('插入关联项目',kwargs['number'])
        except Exception as e:
            db.rollback()
            print('失败', sql)


def get_content(*args, **kwargs):
    for k, v in kwargs.items():
        if kwargs['person'] == 'True':
            temp_data = person_data
        else:
            temp_data = data
        temp_data[k] = v
        json_data = json.dumps(temp_data)
    if args[0] == 'POST':
        rsp = requests.request(args[0], url=args[1], data=json_data, headers=headers)
    else:
        rsp = requests.request(args[0], url=args[1], headers=headers)
    if 'data' not in rsp.text:
        print('请求出错',rsp.text)
        return {'status': 0, 'messae': '请求出错{}'.format(str(kwargs))}
    rsp = rsp.content.decode('utf8')
    rsp = json.loads(rsp)
    if rsp['code'] != 200:
        return {'status': 0, 'messae': '请求出错,cookie过期{}'.format(str(kwargs))}
    return {'status': 1, 'data': rsp['data']}
