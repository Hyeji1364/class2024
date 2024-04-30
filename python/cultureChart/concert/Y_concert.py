import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from datetime import datetime

# 현재 날짜 가져오기
current_date = datetime.now().strftime("%Y-%m-%d")
filename = f"chart_Y_concert10_{current_date}.json"

# 웹드라이버 설정
options = ChromeOptions()
service = ChromeService(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=options)
browser.get("http://ticket.yes24.com/Rank/All")

# 페이지 로드를 위한 대기
time.sleep(5)

# 월간 카테고리 선택
WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[@categoryid='3']"))).click()

# 페이지가 완전히 로드될 때까지 대기
time.sleep(5)

# 새로운 페이지 소스 가져오기
page_source = browser.page_source
# BeautifulSoup을 사용하여 페이지 소스 파싱
soup = BeautifulSoup(page_source, 'html.parser')

# 원하는 데이터 추출 및 처리
concerts_data = []

# 1위부터 3위 정보 추출
rank_best_div = soup.find('div', class_='rank-best')
if rank_best_div:
    concert_divs = rank_best_div.find_all('div')
    for concert_div in concert_divs:
        concert_info = {}
        concert_link = concert_div.find('a', href=True)
        if concert_link:
            concert_info['title'] = concert_link.get('title')
            concert_info['image_url'] = concert_link.find('img')['src']
            concert_info['date_and_location'] = concert_link.find('p', class_='rlb-sub-tit').get_text(strip=True)
            concert_info['rank'] = concert_link.find('p', class_='rank-best-number').find('span').get_text(strip=True)
            concerts_data.append(concert_info)

# 4위부터 10위 정보 추출
rank_list_div = soup.find('div', class_='rank-list')
if rank_list_div:
    concert_divs = rank_list_div.find_all('div', recursive=False)
    for concert_div in concert_divs[:7]:  # 처음 7개 항목만 추출
        concert_info = {}
        concert_link = concert_div.find('a', href=True)
        if concert_link:
            concert_info['title'] = concert_link.find('p', class_='rank-list-tit').text.strip()
            concert_info['image_url'] = concert_link.find('img')['src']
            concert_info['date_and_location'] = concert_div.find('div').find('p').get_text(strip=True)
            concert_info['rank'] = concert_div.find('div', class_='fluctuation').find('span').get_text(strip=True)
            concerts_data.append(concert_info)

# Saving the extracted data to a JSON file
with open(filename, 'w', encoding='utf-8') as file:
    json.dump(concerts_data, file, ensure_ascii=False, indent=4)

# 브라우저 닫기
browser.quit()

print(f"Data saved to {filename}")