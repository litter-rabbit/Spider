# #!/usr/bin/env python
# # -*- encoding: utf-8 -*-
# '''
# @File    :   test.py
# @License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
#
# @Modify Time      @Author     @Desciption
# ------------      -------     -----------
# 2021/1/9 15:39     c-cc        None
# '''
# from selenium import webdriver
#
# from selenium.webdriver.chrome.options import Options  # => 引入Chrome的配置
# import time
# from requests_html import HTMLSession
# from PIL import Image
#
# try:
#     from PIL import Image
# except ImportError:
#     import Image
# import pytesseract
#
# ch_options = Options()
# ch_options.add_argument("--headless")  # => 为Chrome配置无头模式
#
# # 在启动浏览器时加入配置
# driver = webdriver.Chrome()  # => 注意这里的参数
#
# driver.implicitly_wait(5)  # seconds
#
# url=  'http://kd.nsfc.gov.cn/baseQuery/conclusionProject/979a9658900748ba4126341e5bd0d7c5'
# driver.get(url)
#
# time.sleep(2)
#
# try:
#     # 职称所有信息
#     infor_list = driver.find_elements_by_css_selector('#basic-tab > div')
#     all_digital = []
#     for infor in infor_list:
#         infor = infor.text
#         infor = infor.replace("\n",",")
#         all_digital.append(infor)
#
#     all_information = driver.find_elements_by_xpath('//div[@class="tab-pane in active"]/div')
#
#     all_person = []
#     for information in all_information:
#         # 参与人信息
#         person = []
#         information = information.text
#         person.append(information.replace("\n", ","))
#         all_person.append(person)
#
#     print(all_person,all_digital)
# except:
#     pass
# with open("code.txt", "r", encoding="utf-8") as code_file:
# #     codes = code_file.readlines()
# #     with open("content_check.json", "r", encoding="utf-8") as file:
# #         line = file.readlines()[-1]
# #         line = eval(line)
# #     for count in range(len(codes)):
# #         data = codes[count].replace("\n", "")
# #         if data == line["code"]:
# #             code = codes[count + 1].replace("\n", "")
# #
# #             print(code)

def test():

