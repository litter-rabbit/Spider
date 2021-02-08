# #!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   login.py
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author     @Desciption
------------      -------     -----------
2021/1/9 02:42     c-cc        None
'''

from selenium import webdriver

from selenium.webdriver.chrome.options import Options  # => 引入Chrome的配置
import time
from requests_html import HTMLSession
from PIL import Image
import json

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract


class NnsfCheck(object):
    def __init__(self):
        ch_options = Options()
        # ch_options.add_argument("--headless")  # => 为Chrome配置无头模式
        # 在启动浏览器时加入配置
        self.driver = webdriver.Chrome(options=ch_options)  # => 注意这里的参数
        self.driver.implicitly_wait(5)  # seconds

        url = 'http://kd.nsfc.gov.cn/login'

        self.driver.get(url)

        # 进入frame
        self.driver.switch_to.frame(self.driver.find_element_by_css_selector('#iframe_load_data_loginDiv'))

        # 用户名
        self.driver.find_element_by_css_selector('#username').send_keys("528822")

        # 输入密码
        self.driver.find_element_by_css_selector('#password').send_keys("SJTU2020")
        # 点击跳转
        self.driver.find_element_by_css_selector('#indexForm > table > tbody > tr:nth-child(4) > td > input').click()

        image_path = self.driver.find_element_by_css_selector('#validate_img').get_attribute("src")

        # 截图
        self.driver.find_element_by_css_selector('#validate_img').screenshot("image.png")

        # 验证码
        captcha = pytesseract.image_to_string(Image.open('./image.png'))[:-1]
        self.driver.find_element_by_css_selector('#input_default01').send_keys(captcha)

        # 点击跳转
        self.driver.find_element_by_css_selector('#indexForm > table > tbody > tr:nth-child(4) > td > input').click()

        time.sleep(5)

        self.driver.find_element_by_css_selector('#liBaseQuery > a').click()

        time.sleep(1)
        self.driver.find_element_by_css_selector('#collapse-One > div > ul > li:nth-child(2) > a').click()

    def save_to_file(self,item):
        with open("content_check.json","a",encoding="utf-8")as file:
            line = json.dumps(dict(item),ensure_ascii=False) + "\n"
            file.write(line)
            print(line)

    def isElementExist(self, element):
        flag = True
        browser = self.driver
        try:
            browser.find_element_by_xpath(element)
            return flag
        except:
            flag = False
            return flag

    def content_parse(self, driver,path):
        '''
        :param url:
        :return:
        项目详情页
        依次获取字段:
        项目负责人职称
        研究期限
        科研成果
        '''

        driver.implicitly_wait(5)  # seconds
        time.sleep(2)

        # 跳转到新页面
        driver.find_element_by_xpath(path).click()
        # 获取所有的

        # 当前打开的所有窗口
        windows = driver.window_handles
        # 转换到最新打开的窗口
        driver.switch_to.window(windows[-1])

        try:
            '''
            根据查找的代码查找
            '''
            # 职称所有信息
            infor_list = driver.find_elements_by_css_selector('#basic-tab > div')

            # 所有关键字细节
            # all_digital = []
            # for infor in infor_list:
            #     all_digital.append(infor.text)
            #

            all_information = driver.find_elements_by_xpath('//div[@class="tab-pane in active"]/div')

            '''
            所有参与人的信息            
            '''
            all_person = []
            for information in all_information:
                '''
                获取参与人，姓名，单位名称，职称
                '''
                information.find_element_by_css_selector('#participatantsList-tab > div > div > a').click()
                time.sleep(2)
                # 当前打开的所有窗口
                windows = driver.window_handles
                # 转换到最新打开的窗口
                driver.switch_to.window(windows[-1])

                # 个人简介
                intorduces = driver.find_elements_by_css_selector('#admin-basic-tab > div')

                all_intorduce = []
                for intorduce in intorduces:
                    all_intorduce.append(intorduce.text)

                # 参与项目点击
                driver.find_element_by_xpath('//a[contains(text(),"参与项目")][1]').click()
                time.sleep(2)
                # 他人主持的项目卡片册
                project_list = driver.find_elements_by_xpath('//div[@id="listDivN"]')
                all_people_project_list = []
                for project in project_list:

                    title = project.find_element_by_xpath('//h4').text
                    project_category = project.find_element_by_xpath('//div[contains(text(),"项目类别：")]').text
                    project_code = driver.find_element_by_xpath('//div[contains(text(),"批准号：")]').text
                    date_year = driver.find_element_by_xpath('//div[contains(text(),"批准年度")]').text

                    salary = driver.find_element_by_xpath('//div[contains(text(),"资助经费：")]').text

                    unit = driver.find_element_by_xpath('//div[contains(text(),"依托单位：")]/a').text
                    main = driver.find_element_by_xpath('//div[contains(text(),"项目负责人：")]/a').text

                    participants = dict()

                    participants["描述信息"] = all_intorduce
                    participants["标题"] = title
                    participants["批准号"] = project_code
                    participants["项目类别"] = project_category
                    participants["批准年度"] = date_year
                    participants["资助经费"] = salary
                    participants["依托单位"] = unit
                    participants["项目负责人"] = main

                    all_people_project_list.append(participants)

                    # 关闭浏览器窗口返回上一页

                    driver.close()

                    # 当前打开的所有窗口
                    windows = driver.window_handles
                    # 转换到最新打开的窗口
                    driver.switch_to.window(windows[-1])

                all_person.append(all_people_project_list)



            driver.close()

            windows = driver.window_handles
            # 转换到最新打开的窗口
            driver.switch_to.window(windows[-1])
            return all_person


        except:
            pass

    def run(self):
        with open("code.txt","r") as code_get:
            codes = code_get.readlines()
            for code in codes:
                '''
                抓取前判断是否已经抓取了此编号
                '''
                code = code.replace("\n","")

                if len(code) == 8:
                    # 检查之前是否已经抓取过该信息
                    with open("code.txt", "r", encoding="utf-8") as code_file:
                        codes = code_file.readlines()
                        with open("content_check.json", "r", encoding="utf-8") as file:
                            line = file.readlines()[-1]
                            line = eval(line)
                        for count in range(len(codes)):
                            data = codes[count].replace("\n", "")
                            if data == line["code"]:
                                code = codes[count + 1].replace("\n", "")
                                # 初始刷新页面
                                self.driver.refresh()
                                # 当前打开的所有窗口
                                windows = self.driver.window_handles
                                # 转换到最新打开的窗口
                                self.driver.switch_to.window(windows[-1])
                                self.driver.find_element_by_css_selector('#ratificationNo').click()
                                self.driver.find_element_by_css_selector('#ratificationNo').send_keys(code)

                                self.driver.find_element_by_css_selector(
                                    '#query-input > div > div:nth-child(2) > div:nth-child(6) > button').click()

                                time.sleep(3)

                                # 获取解题项目
                                try:
                                    if self.isElementExist('//div[contains(text(),"结题项目：")]/a'):
                                        content_page = self.driver.find_elements_by_xpath('//div[contains(text(),"结题项目：")]/a')
                                        all_data = self.content_parse(self.driver, '//div[contains(text(),"结题项目：")]/a')
                                        data = dict()
                                        data["code"] = code
                                        data["information"] = all_data
                                        self.save_to_file(data)

                                except Exception as err:
                                    print(err)


if __name__ == '__main__':
    check = NnsfCheck()
    check.run()
