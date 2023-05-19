#django
from django.db import models

#selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# #BeautifulSoup && normalization
from bs4 import BeautifulSoup
import re

# etc
import time
import os

def driver_setting():
    global driver
    driver = Options()
    driver.add_experimental_option("detach", True)  # 브라우저 바로 닫힘 방지
    driver.add_experimental_option("excludeSwitches", ["enable-logging"])  # 불필요한 메시지 제거
    driver.add_argument('--blink-settings=imagesEnabled=false')
    driver.add_argument("window-size=1920x1080")
    driver.add_argument('headless')
    driver.headless = True
    driver.add_argument(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
    driver = webdriver.Chrome()


def login(id, passwd):
    driver.get("https://portal.dju.ac.kr/index.jsp")

    # 포탈 접속 입력
    id_tag = driver.find_element(By.CLASS_NAME, "id_input1")
    passwd_tag = driver.find_element(By.CLASS_NAME, "id_input2")
    id_tag.send_keys(id)
    passwd_tag.send_keys(passwd)
    passwd_tag.send_keys(Keys.ENTER)
    time.sleep(0.5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='homeLink']")))

def search_portal():
    # 통합 정보 시스템 접속
    driver.find_element(By.XPATH, "//*[@id='homeLink']").click()
    time.sleep(0.3)

    # 통합 정보 시스템 인증 절차 때문에 xml파일 파싱 불가. 새 탭을 여는 방식
    driver.get("https://itics.dju.ac.kr/main.do")
    driver.switch_to.window(driver.window_handles[0])
    
    # 검색창 키워드 찾기
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mainframe_waitwindow")))
    time.sleep(0.3)
    
    # 성적 조회 창 접속
    search_keyword = driver.find_element(By.TAG_NAME,"input")
    search_keyword.click()
    search_keyword.send_keys("전체성적조회")
    search_keyword.send_keys(Keys.ENTER)
    time.sleep(0.3)

    # 성적 보드 frame 찾기
    driver.find_element(By.ID,
                        "mainframe_childframe_form_leftContentDiv_widType_BTN_SEARCH_MENU_DIV_menuDiv_DG_LEFT_MENU_body_gridrow_1").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.ID, "mainframe_childframe_form_mainContentDiv_workDiv_WINB010603_INFODIV01_INFODIV01_Title00")))
    time.sleep(0.3)


def parsing():
    with open("media/userXML/crypto.html", "w", encoding="utf8") as f:
        f.write(driver.page_source)
    soup = BeautifulSoup(driver.page_source, "lxml")

def delete_xml():
    file_path = 'media/userXML/crypto.html'
    if os.path.isfile(file_path):
        os.remove(file_path)

# main
def getStudentScore(id, passwd):
    while(True):
        try:
            driver_setting()
            login(id, passwd)
            search_portal()
            parsing()
            delete_xml()
            break
        except Exception as e:
            print("예외 발생 : " + e)