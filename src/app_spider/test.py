
import requests
kw="王者荣耀"
pns= pns_sequences = ['', 'MTA', 'MjA', 'MzA', 'NDA', 'NTA', 'NjA', 'NzA', 'ODA', 'OTA', 'MTAw', 'MTEw', 'MTIw', 'MTMw','MTQw']
url = "https://sj.qq.com/myapp/searchAjax.htm?kw="+str(kw)+"&pns="+str(pns[6])+"&sid="
url='https://appgallery.huawei.com//static/2020121619/js/app.c827496f74b216975982.js'
def test():

    headers = {
        "user-agent":"user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
    }


    rsp=requests.get(url,headers=headers)
    print(rsp.content.decode('utf-8'))


if __name__ == '__main__':
    test()