import requests

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from requestium import Session, Keys, Select

from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys


import json
import os
def login():
    driver = webdriver.Chrome()
    driver.get('https://qun.qq.com/')
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div/p[1]/a').click()
    time.sleep(2)
    if os.path.exists('707.png'):
        os.remove('707.png')
    driver.get_screenshot_as_file('707.png')
    time.sleep(20)
    cookie=driver.get_cookies()
    print(cookie)
    c=''
    try:
        for i in cookie:
            if i['name']=='skey':
                skey = '{}={}'.format(i['name'], i['value'])
            elif i['name']=='uin':
                uin='{}={}'.format(i['name'],i['value'])

        c=uin+';'+skey
    except Exception as e:
        c=''

    driver.quit()
    return c



def change_profile(s):
    usa=s.driver.ensure_element_by_id('country',state='visible')
    Select(usa).select_by_value('US')
    s.driver.find_element_by_xpath('//*[@id="__next"]/div[4]/div/div[2]/div[2]/div[2]/div/article/section/form/div/button').click()



def confirm_address(s,link):

    s.driver.get(link)
    s.driver.find_element_by_tag_name('input').send_keys('1')
    s.driver.find_elements_by_tag_name('button')[1].click()
    time.sleep(1)
    s.driver.find_element_by_xpath('//*[@id="confirm-address-dialog"]/footer/button[2]').click()



def run():
    s=login('kuaixi3995285@163.com','07551012')
    change_profile(s)
    link='https://www.spotify.com/us/family/join/address/YAB97cbAZ168zbZ/'
    confirm_address(s,link)





if __name__ == '__main__':

    c=login()
    print(c)