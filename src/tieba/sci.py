import requests
import traceback
from src.sci.utils import get_content, insert_project, get_db
import pickle
query_url = "http://kd.nsfc.gov.cn/baseQuery/data/supportQueryResultsData"

info_url = "http://kd.nsfc.gov.cn/baseQuery/data/conclusionProjectInfo/{}"

person_info_url = "http://kd.nsfc.gov.cn/advancedQuery/data/supportQueryPersonResultsData"

person_participate_url = "http://kd.nsfc.gov.cn/advancedQuery/data/supportQueryParticipateResultsData"
import time


# 存储project表
def get_project_partipage():
    with open('code8596.txt', 'r') as f:
        for number_id in f.readlines():
            time.sleep(0.1)
            number_id = number_id.strip()
            rsp = get_content('POST', query_url, ratifyNo=number_id, person='False')
            if rsp['status'] == 0:
                print('请求出错', rsp)
                return
            if not rsp['data']['resultsData']:
                print('数据不存在')
                continue
            query_rsp = rsp['data']['resultsData'][0]
            info_rsp = get_content('GET', info_url.format(query_rsp[0]))['data']
            p = dict()
            p['number'] = number_id
            p['position'] = info_rsp['adminPosition']
            p['study_duration'] = info_rsp['researchTimeScope']
            p['study_result'] = query_rsp[10]
            p['admin_id'] = query_rsp[12]
            p['title'] = query_rsp[1]
            p['group'] = query_rsp[14]
            p['catetory'] = query_rsp[3]
            p['money'] = query_rsp[6]
            p['master'] = query_rsp[5]
            p['company'] = query_rsp[4]
            p['year'] = query_rsp[7]
            print(p)
            insert_project('project', **p)
            participatantsList = info_rsp['participatantsList']
            for person in participatantsList:
                person_detail = person['result']
                person_dict = {}
                person_dict['person_id'] = person_detail[0]
                person_dict['name'] = person_detail[1].replace("'"," ")
                person_dict['position'] = person_detail[2]
                person_dict['company'] = person_detail[4].replace("'", "")
                person_dict['number_key'] = number_id

                insert_project('part_person', **person_dict)


#
# def get_project_partipage(sub_list):
#
#     for number_id in sub_list:
#         print('正在处理',number_id)
#         time.sleep(1)
#         number_id = number_id.strip()
#         rsp = get_content('POST', query_url, ratifyNo=number_id, person='False')
#         if rsp['status'] == 0:
#             print('请求出错', rsp)
#             return
#         if not rsp['data']['resultsData']:
#             print('数据不存在')
#             continue
#         query_rsp = rsp['data']['resultsData'][0]
#         info_rsp = get_content('GET', info_url.format(query_rsp[0]))['data']
#         p = dict()
#         p['number'] = number_id
#         p['position'] = info_rsp['adminPosition']
#         p['study_duration'] = info_rsp['researchTimeScope']
#         p['study_result'] = query_rsp[10]
#         p['admin_id'] = query_rsp[12]
#         p['title'] = query_rsp[1]
#         p['group'] = query_rsp[14]
#         p['catetory'] = query_rsp[3]
#         p['money'] = query_rsp[6]
#         p['master'] = query_rsp[5]
#         p['company'] = query_rsp[4]
#         p['year'] = query_rsp[7]
#         print(p)
#         insert_project('project', **p)
#         participatantsList = info_rsp['participatantsList']
#         for person in participatantsList:
#             person_detail = person['result']
#             person_dict = {}
#             person_dict['person_id'] = person_detail[0]
#             person_dict['name'] = person_detail[1]
#             person_dict['position'] = person_detail[2]
#             person_dict['company'] = person_detail[4].replace("'", "")
#             person_dict['number_key'] = number_id
#
#             insert_project('part_person', **person_dict)



def get_person_participate():
    db = get_db()
    cursor = db.cursor()
    sql = "select number,admin_id from project "
    cursor.execute(sql)
    res = cursor.fetchall()
    print(res)
    for number, admin_id in res:
        time.sleep(0.1)
        print(number)
        print(admin_id)
        person_rsp = get_content('POST', person_info_url, adminID=admin_id, person='False')
        participate_rsp = get_content('POST', person_participate_url, adadminID=admin_id, id=admin_id, person='True')
        if person_rsp['status'] == 1 and participate_rsp['status'] == 1:
            person_rsp_list = person_rsp['data']['resultsData']
            part_rsp_list = participate_rsp['data']['resultsData']
            for p_rsp in person_rsp_list:
                p = {}
                print('p_rsp', p_rsp)
                p['title'] = p_rsp[1]
                p['number'] = p_rsp[2]
                p['year'] = p_rsp[7]
                p['catetory'] = p_rsp[14]
                p['money'] = p_rsp[6]
                p['master'] = p_rsp[5]
                p['company'] = p_rsp[4]
                p['number_key'] = number
                p['is_master'] = 1
                insert_project('rela_project', **p)
            for person_rsp in part_rsp_list:
                p = {}
                p['title'] = person_rsp[1]
                p['number'] = person_rsp[2]
                p['year'] = person_rsp[7]
                p['catetory'] = person_rsp[14]
                p['money'] = person_rsp[6]
                p['master'] = person_rsp[5]
                p['company'] = person_rsp[4]
                p['number_key'] = number
                p['is_master'] = 0
                insert_project('rela_project', **p)


def pickel():
    result = []


    with open('code.txt') as f:
        for line in f.readlines():
            line = line.strip()
            result.append(line)
    f = open('pic_code.txt','wb')
    pickle.dump(result,f)

def get_pic():

    result = pickle.load(open('pic_code.txt','rb'))


# def run():
#     from threading import Thread
#     result = pickle.load(open('pic_code.txt', 'rb'))
#     sub_list =[]
#     gap = int(len(result)/10)
#     for i in range(10):
#         temp_list = result[i*gap:(i+1)*gap]
#         sub_list.append(temp_list)
#
#     thread_list  = []
#     for i in sub_list:
#         t = Thread(target=get_project_partipage,args=(i,))
#         thread_list.append(t)
#     for t in thread_list:
#         t.start()
#
#     for t in thread_list:
#         t.join()


if __name__ == '__main__':
    get_project_partipage()



