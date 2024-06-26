import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from datetime import datetime
import time

# 웹 드라이버 설정
options = ChromeOptions()
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
url = "https://ticket.melon.com/ranking/index.htm"

# 웹 페이지에 접속
driver.get(url)
time.sleep(5)  # 페이지 로딩 대기

# "뮤지컬/연극" 섹션으로 전환
button_exh_classic_etc = driver.find_element(By.CSS_SELECTOR, 'button[value="NEW_GENRE_ART"]')
button_exh_classic_etc.click()
time.sleep(2)  # 섹션 변경 후 데이터 로딩 대기

# 스크롤 다운을 통한 모든 데이터 로딩 (필요한 경우)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)

# 필요한 데이터 수집
data = []
rows = driver.find_elements(By.CSS_SELECTOR, '.tbl.tbl_style02 tbody tr')
for row in rows:
    rank = row.find_element(By.CSS_SELECTOR, 'td.fst .ranking').text.strip()
    title = row.find_element(By.CSS_SELECTOR, 'div.show_infor p.infor_text a').text.strip()
    image = row.find_element(By.CSS_SELECTOR, 'div.thumb_90x125 img').get_attribute('src')
    venue = row.find_element(By.CSS_SELECTOR, 'td:nth-child(4)').text.strip()

    data.append({
        'Rank': rank,
        'Title': title,
        'Venue': venue,
        'ImageURL': image
    })

# JSON 파일로 저장
current_date = datetime.now().strftime("%Y-%m-%d")
filename = f"chart_M_musical_{current_date}.json"
with open(filename, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

# 드라이버 종료
driver.quit()

# 출력 결과 확인
for item in data:
    print(item)