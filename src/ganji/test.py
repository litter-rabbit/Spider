

import requests


def get_ip():
    r=requests.request('GET',url='http://121.199.4.165:5555/random')
    return  r.text

headers={
    'Cookie': 'ganji_xuuid=505208bb-1334-4b9b-ca2b-154dc493449c.1588832367087; ganji_uuid=1241764887537716486526; lg=1; sscode=YEte4WBKwTb6HWz7YEOYFh8J; GanjiUserName=%23qq_812497091; GanjiUserInfo=%7B%22user_id%22%3A812497091%2C%22email%22%3A%22%22%2C%22username%22%3A%22%23qq_812497091%22%2C%22user_name%22%3A%22%23qq_812497091%22%2C%22nickname%22%3A%22%5Cu6c89%5Cu9ed8%5Cuff5e%5Cu65e0%5Cu8bed%22%7D; bizs=%5B%5D; last_name=%23qq_812497091; xxzl_deviceid=ApcpjGocIFyn8HasF%2BSEatFvrIc7q6yLezqSap4gGw7DtGUNyKCvIX8XsxUFDlJp; xxzl_smartid=399fd109f632128de82a7d74daace9d7; gj_footprint=%5B%5B%22%5Cu5bb6%5Cu6559%22%2C%22%5C%2Fjzjiajiaolaoshi%5C%2F%22%5D%5D; ParttimeWantedListPageScreenType=1536; __gads=ID=a911cf55249984cb:T=1588835611:S=ALNI_MaoIAKDhbLrAXV9hKoHTE2yDS-fmQ; _gl_tracker=%7B%22ca_source%22%3A%22www.google.com%22%2C%22ca_name%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_id%22%3A%22-%22%2C%22ca_s%22%3A%22seo_google%22%2C%22ca_n%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22sid%22%3A78281318461%7D; GANJISESSID=anrest1qr86mu6aopda23kirj2; __utma=32156897.1811114207.1588832372.1588842120.1588859087.3; __utmc=32156897; __utmz=32156897.1588859087.3.3.utmcsr=jiujiang.ganji.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmt=1; citydomain=bj; ganji_login_act=1588859330591; _gl_speed=%5B%22https%3A%2F%2Fjxjump.58.com%2Fservice%3Ftarget%3DFCADV8oV3os7xtAjgt1OATkB9Bw0MJvFUpAswz1-fENN44j_Zpk1zEffDjpdRkNz3Q5xoKYl4Bi0ja0SaVzN_Bqqd9VtbaaBozRC5yBP1ZKMCGY1NYlL9SMDQpW05iOImbLKgeEvZYetOdm6ZHg1njrLCa4ukfCbRGVaWhwAwIAsnVFVGVkJ-frjEcIsiu1SCX0XjH4ihD5CgSbgjvrimpcCXDUgnTnuV4ut2oMzJts5psgUftKxL_14UhQ%26pubid%3D0%26apptype%3D10%26psid%3D106828863208254969966887488%26entinfo%3D41858326103074_0%26cookie%3D%7C%7C%7C1241764887537716486526%26fzbref%3D0%26key%3D%26params%3Drank0830gspanxuan0099%5Edesc%26gjcity%3Dbj%22%2C1588859447112%5D; __utmb=32156897.17.10.1588859087',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
}

proxies={
    'http':'http://'+get_ip()
}




def test():
    url='https://bj.ganji.com/zufang/41858326103074x.shtml?entinfo=41858326103074_0&fzbref=0&params=rank0830gspanxuan0099^desc&gjcity=bj&psid=106828863208254969966887488&cookie=|||1241764887537716486526&apptype=10&key=&pubid=0&trackkey=41858326103074_e5bc077f-875c-4025-95ff-642cca41687a_20200507215047_1588859447570&fcinfotype=gz&jingxuan=1'
    reponse=requests.request('GET',url=url)
    for i in range(50):
        reponse = requests.request('GET', url=url,proxies=proxies)
        if reponse.status_code ==200:
            print('OK')
        else:
            print('Bad')








if __name__ == '__main__':

    test()