import requests
# @mnuXbO3i7

headers = {
    'cookie':'uin=o3169267862;skey=@kXEAeZiUa;p_uin=o3169267862;p_skey=NVl0*CycWcr7TEPGdmIAZDQE4wzm-uY6W6KlFJj0l*I_'

}

url = 'https://qun.qq.com/cgi-bin/qun_mgr/get_group_list'
cookie='uin=o3091376103;skey=@fAOMESg8T;p_uin=o3091376103;p_skey=fxdabc03Xunl0tltnvus8yMcMQsEjwyGvD-Jl39-fgY_'
url='https://qun.qq.com/cgi-bin/group_search/pc_group_search'

import sys
import json
def run():

    data = {
        'keyword':'142414598',
        'from': '1',
        'wantnum': '24',
    }
    res = requests.post(url=url, headers=headers, data=data)
    print(res.status_code)
    res=res.content.decode('utf-8')
    res=json.loads(res)
    print(res)
    active=res['group_list'][0]['activity']
    qq=res['group_list'][0]['code']
    group_label_list=res['group_list'][0]['group_label']
    try:
        label_list=res['group_list'][0]['labels']
    except Exception as e:
        label_list = ''
    name=res['group_list'][0]['name']
    logo=res['group_list'][0]['url']
    info_list=res['group_list'][0]['gcate']
    print(active)
    print(qq)
    print(group_label_list)
    print(label_list)
    print(name)
    print(logo)
    print(info_list)




if __name__ == '__main__':
    run()
