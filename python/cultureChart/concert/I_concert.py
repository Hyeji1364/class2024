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
filename = f"chart_I_concert10_{current_date}.json"
# 웹드라이버 설정
options = ChromeOptions()
service = ChromeService(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=options)
browser.get("https://tickets.interpark.com/contents/ranking")
# RadioButton_wrap__761f0 클래스를 가진 div 요소를 찾기
search_box = browser.find_element(By.CLASS_NAME, "RadioButton_wrap__761f0")
# "콘서트" 탭 버튼을 찾아서 클릭하기
try:
    concert_tab_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='콘서트']"))
    )
    concert_tab_button.click()
    print("Clicked '콘서트' tab.")
    time.sleep(3)  # 페이지가 완전히 로드될 때까지 대기
except Exception as e:
    print("Error clicking '콘서트' tab:", e)
# "월간" 탭 버튼을 찾아서 클릭하기
try:
    monthly_tab_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='월간']"))
    )
    monthly_tab_button.click()
    print("Clicked '월간' tab.")
    time.sleep(3)  # 페이지가 완전히 로드될 때까지 대기
except Exception as e:
    print("Error clicking '월간' tab:", e)
time.sleep(3)
# 페이지 소스 가져오기
page_source = browser.page_source
# BeautifulSoup을 사용하여 HTML 파싱
soup = BeautifulSoup(page_source, 'html.parser')