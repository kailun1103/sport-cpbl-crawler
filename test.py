from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import datetime
import requests
import json
import time
import csv
import os


# ---------------------------------參數設定---------------------------------
cpbl_driver = webdriver.Chrome()
cpbl_driver.get('https://www.cpbl.com.tw/stats/recordall')


time.sleep(5)
cpbl_soup = BeautifulSoup(cpbl_driver.page_source, "html.parser")



# ---------------------------------開始爬蟲---------------------------------
# 選取所有需要的元素
ranks = cpbl_soup.select('.rank')[1:]  # 從第二個元素開始
teams = cpbl_soup.select('.team_logo')
names = cpbl_soup.select('.name')
nums = cpbl_soup.select('.num')[27:]  # 從第28個元素開始

# 分組 nums 列表
num_groups = []
for i in range(0, len(nums), 27):
    num_groups.append(nums[i:i+27])

# 使用 zip 函數將列表合併
elements = zip(ranks, teams, names, num_groups)

# 迭代所有元素
for rank, team, name, num_group in elements:
    rank_text = rank.get_text(strip=True) # strip=True 是 get_text() 方法的一個參數,用於去除文本前後的空白字符
    team_text = team.get_text(strip=True)
    name_text = name.get_text(strip=True)
    num_texts = [num.get_text(strip=True) for num in num_group]
    print(f'排名: {rank_text}')
    print(f'球隊: {team_text}')
    print(f'球員: {name_text}')
    print(f'球員數據: {", ".join(num_texts)}')
    print('-' * 80)

# ---------------------------------準備寫入csv?---------------------------------