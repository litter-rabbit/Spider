import requests

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from requestium import Session, Keys, Select





def login(email,password):

    s = Session('./chromedriver.exe', browser='chrome', default_timeout=15)
    s.driver.get('https://accounts.google.com/signin/v2/identifier?hl=zh-CN&continue=https%3A%2F%2Fmail.google.com%2Fmail&service=mail&flowName=GlifWebSignIn&flowEntry=AddSession')
    inputs=s.driver.find_elements_by_tag_name('input')
    inputs[0].send_keys(email)



    return s



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
    login('123','11')
