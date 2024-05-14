from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import csv

# ---------------------------------第一步: Selenium參數設定---------------------------------
cpbl_driver = webdriver.Chrome()
cpbl_driver.get('https://www.cpbl.com.tw/stats/recordall')
cpbl_driver.maximize_window() # 放大視窗
time.sleep(5)

# ---------------------------------第二步: Selenium網頁設定---------------------------------
# 點擊頁數選取器
page_element = WebDriverWait(cpbl_driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="PageSize"]'))
)
page_element.click()
# 點擊60頁的選項
sixty_perPage_element = WebDriverWait(cpbl_driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="PageSize"]/option[4]'))
)
sixty_perPage_element.click()
# 點擊確認
check_element = WebDriverWait(cpbl_driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="SendTextPaging"]'))
)
check_element.click()
time.sleep(5)

# ---------------------------------第三步: BeautifulSoup參數設定---------------------------------
cpbl_soup = BeautifulSoup(cpbl_driver.page_source, "html.parser")
time.sleep(5)

# ---------------------------------第四步: BeautifulSoup爬蟲---------------------------------
# 剖析當前cpbl_driver視窗的HTML，並且選取所有需要的元素
ranks = cpbl_soup.select('.rank')[1:]  # 從第二個元素開始
teams = cpbl_soup.select('.team_logo')
players = cpbl_soup.select('.name')
states = cpbl_soup.select('.num')[27:]  # 從第28個元素開始

# 分組 nums 列表
states_groups = []
for i in range(0, len(states), 27):
    states_groups.append(states[i:i+27])

# 使用 zip 函數將列表合併
elements = zip(ranks, teams, players, states_groups)

# ---------------------------------第五步: 準備寫入csv---------------------------------

with open('test.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['排名', '球隊', '球員', '打擊率', '出賽數', '打席', '打數', '得分', '打點', '安打', '一安', '二安', '三安', '全壘打', '累打數', '長打數', '四壞', '(故四)', '死球', '被三振', '雙殺打', '犧短', '犧飛', '盜壘', '盜壘刺', '上壘率', '長打率', '整體攻擊指數', '滾飛出局比', '保送三振比'])

    # 迭代所有元素
    for rank, team, players, states_group in elements:
        rank_text = rank.get_text(strip=True) # strip=True 是 get_text() 方法的一個參數,用於去除文本前後的空白字符
        team_text = team.get_text(strip=True)
        players_text = players.get_text(strip=True)
        states_texts = [states.get_text(strip=True) for states in states_group]
        print(f'排名: {rank_text}')
        print(f'球隊: {team_text}')
        print(f'球員: {players_text}')
        print(f'球員數據: {", ".join(states_texts)}')
        print('-' * 80)

        # 寫入 CSV，每個 states_texts 元素作為一個單獨的列
        csv_writer.writerow([rank_text, team_text, players_text] + states_texts)