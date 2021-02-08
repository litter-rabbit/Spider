import requests

headers1 = {
    'cookie': 'RK=czY4M9WmNk; ptcz=e80008226e1929ff44bb6f265e561346557be6c546fd8576c19446002590ce7f; pgv_pvi=9691181056; pgv_pvid=6817797190; eas_sid=61Y59969U2U8u0d5t0g2d9k3c4; ied_qq=o1657165940; uin_cookie=o1657165940; tvfe_boss_uuid=49f72d4d108c0db7; o_cookie=1657165940; LW_sid=J1d6Q0B0y2L5R1f6k4w9D8h3n7; LW_uid=w1i6H0g0P2Y5Y1V654Q938O3G9; psrf_qqunionid=; euin=oKCk7i6s7KEPon**; psrf_qqopenid=8978AE926E7A4ED22A7908260D3CFCC5; tmeLoginType=2; psrf_access_token_expiresAt=1610681638; psrf_qqrefresh_token=51F7CAE270D9F5BCB6875169722B2770; psrf_qqaccess_token=5548EA610FCB6E5CF8AB119CFAA5F306; _qpsvr_localtk=1606442780882; traceid=dad2991b6d'
}

headers = {
    'cookie': 'pgv_pvi=1588443136; RK=oU5s5+w2e3; ptcz=1945f4464b337f292e704c9873044e121f283a1ada91894421313c658d699038; pgv_pvid=1857479990; eas_sid=D1V568O8q0j4x83878I6A0Z4I7; LW_uid=X1D5X8V9X3S0G8w5R6j3T7e2Z7; tvfe_boss_uuid=6d29289922fe4d86; uin_cookie=o0709343607; ied_qq=o0709343607; o_cookie=709343607; pac_uid=1_709343607; iip=0; ptui_loginuin=709343607; pgg_uid=158075519; pgg_appid=101503919; pgg_openid=5F0A72EF48243739FE12794CDD2A0E82; pgg_access_token=C22233BC461454816080A600BDEF7908; pgg_type=1; pgg_user_type=5; LW_sid=G1C640u083t1l9a9f1d441n6s8; _qpsvr_localtk=0.667078159871247; uin=o0709343607; skey=@VFeXsqVIc; p_uin=o0709343607; pt4_token=kFWglcEVlEkWqWv7Zm8izPVmFyYkElkgpvh47qx0Zy0_; p_skey=Md4g72xgOsive*Y-87LdJmQ7gipgDCQ9Xnk*RHugcXg_; traceid=6667bd2825'
}

headers2 = {
    'cookie': 'RK=EHrUZcPcwC; ptcz=770c291d0176944db24159dfee2db97e8a009acb48f33196723a9b4739793526; pgv_pvid=5852437540; pgv_pvi=6342369280; iip=0; tvfe_boss_uuid=063aaa6f227bd9e9; eas_sid=Q1z559W7H310V4q9w0T293o5N3; uin_cookie=o3013479439; ied_qq=o3013479439; o_cookie=3013479439; pac_uid=1_3013479439; psrf_qqunionid=; psrf_qqrefresh_token=791B7C8A0377812757D2FE35F2A84FF4; euin=oin5oivlNKviNv**; psrf_qqopenid=4370A01A97D434143B3275F969FE5EB3; psrf_qqaccess_token=D7FFF86095A24D3C8181882D1206E622; tmeLoginType=2; psrf_access_token_expiresAt=1608531091; _qpsvr_localtk=1606439334601; traceid=bd48baa453'
}
data = {
    'keyword': '928924122',
    'from': '1',
    'wantnum': '24',
}

url = 'https://qun.qq.com/cgi-bin/group_search/pc_group_search'

session = requests.session()

import json


def run():
    res = session.get('https://find.qq.com/')
    cookie=res.cookies
    for key,value in cookie.items():
        print(value)


    # res = session.post(url=url, headers=headers, data=data)
    # print(res.status_code)
    # res = res.content.decode('utf-8')
    # res = json.loads(res)
    # print(res)
    # active = res['group_list'][0]['activity']
    # qq = res['group_list'][0]['code']
    # group_label_list = res['group_list'][0]['group_label']
    # try:
    #     label_list = res['group_list'][0]['labels']
    # except Exception as e:
    #     label_list = res['group_list'][0]['labels']
    #
    # name = res['group_list'][0]['name']
    # logo = res['group_list'][0]['url']
    # info_list = res['group_list'][0]['gcate']
    # print(active)
    # print(qq)
    # print(group_label_list)
    # print(label_list)
    # print(name)
    # print(logo)
    # print(info_list)


if __name__ == '__main__':
    run()
