import requests

# url = "http://kd.nsfc.gov.cn/baseQuery/data/supportQueryResultsData"
#
# url_user_info = "http://kd.nsfc.gov.cn/baseQuery/data/conclusionProjectInfo/779bfab590d085dc83f5fb95fb79ed2c"
#
# data = {
#     "adminID": "",
#     "beginYear": "",
#     "checkDep": "",
#     "checkType": "",
#     "code": "",
#     "complete": "true",
#     "conclusionYear": "",
#     "dependUnit": "",
#     "endYear": "",
#     "keywords": "",
#     "pageNum": 0,
#     "pageSize": 5,
#     "personInCharge": "",
#     "projectName": "",
#     "projectType": "",
#     "psPType": "",
#     "queryType": "input",
#     "quickQueryInput": "",
#     "ratifyNo": "71172088",
#     "ratifyYear": "",
#     "subPType": "",
#
# }
# import json
# data = json.dumps(data)
#
# headers = {
#     "Content-Type": "application/json",
#     "Origin": "http://kd.nsfc.gov.cn",
#     "Cookie": "JSESSIONID=6C23C6F39F54BF3D5C944E2C3822C1EC",
#     "Origin": "http://kd.nsfc.gov.cn",
#     "Referer": "http://kd.nsfc.gov.cn/baseQuery/conclusionQuery",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
# }
# rsp = requests.request('POST', url=url,data=data,headers=headers)
# print(rsp.text)
# # 71202149
# def testuser():
#     rsp = requests.request('GET', url=url_user_info,headers=headers)
#     print(rsp.text)


def get_next_file(number_id):
    flag = 0
    f_w = open('code8596.txt','w')
    with open('code.txt','r') as f:
        for lien in f.readlines():
            line = lien.strip()
            if flag or line==str(number_id):
                flag=1
                f_w.write(line)
                f_w.write('\n')





if __name__ == '__main__':
    get_next_file(21402126)