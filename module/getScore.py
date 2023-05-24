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
import selenium_async

#except
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import InvalidSessionIdException
from selenium.common.exceptions import TimeoutException

#
from celery import shared_task

# etc
import hashlib
import time
import os

@shared_task
def get_selenium(id, passwd, url):

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"

    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])  # 불필요한 메시지 제거
    options.add_argument('--blink-settings=imagesEnabled=false')
    # options.add_argument('headless')
    options.add_argument('user-agent='+ user_agent)

    driver = webdriver.Chrome(options=options)



    driver.get(url)

    # 포탈 접속 입력
    id_tag = driver.find_element(By.CLASS_NAME, "id_input1")
    passwd_tag = driver.find_element(By.CLASS_NAME, "id_input2")
    id_tag.send_keys(id)
    passwd_tag.send_keys(passwd)
    passwd_tag.send_keys(Keys.ENTER)
    time.sleep(0.5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='homeLink']")))


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



    filename = hashlib.md5(id.encode()).hexdigest()
    with open(f'media/userXML/{filename}.html', "w", encoding="utf8") as f:
        f.write(driver.page_source)

    soup = BeautifulSoup(driver.page_source, "lxml")

    driver.quit()
    allScore = {}
    semester = ["classification", "class_num", "subject", "div_class", "credit", "grade", "score", "rating"]
    figure = ["req_credit","acq_creidt","rating_cnt","rating_avg","r_scores","r_scores_avg","per_score"]

    for i in range(16):
        allScore[i] = {"name":"", "semester": {}, "figure": {},}

        # semester(score)
        for j in range(12):
            try:
                finds_text = soup.find_all(id=re.compile(
                    'INFODIV01_INFODIV01_DG_GRID{0}_body_gridrow_._cell_._{1}GridCellTextContainerElement'.format(
                        str(i).zfill(2), j)))

                allScore[i]["semester"]['{}'.format(semester[j])] = [find_text.get_text().strip() for find_text in
                                                                   finds_text]
            except:
                print("과목 끝")
                # 과목 끝
                break

        # name
        try:
            finds_text = soup.find(
                id=re.compile('INFODIV01_INFODIV01_Title{}TextBox'.format(str(i).zfill(2)))).get_text().strip()
            allScore[i]["name"] = finds_text
        except:
            print("학기 이름 끝")
            # 학기 이름 끝
            break

        # figure (all)
        finds_text = soup.find(
            id=re.compile('INFODIV01_INFODIV01_Sum{}TextBoxElement'.format(str(i).zfill(2)))).get_text().replace(" ", "").split(
            "*")
        finds_text = list(filter(None, finds_text)) # 공백 생겨서 없애는 과정

        for f in range(len(finds_text)):
            pattern1 = re.compile("\d+.\d+")
            finds_text[f] = pattern1.search(finds_text[f]).group()
            allScore[i]["figure"]["{}".format(figure[f])] = finds_text[f]

    allScore.popitem() # try 예외 처리에서 생성된 빈 공간 제거



    #파일 삭제
    filename = hashlib.md5(id.encode()).hexdigest()
    file_path = f'media/userXML/{filename}.html'
    if os.path.isfile(file_path):
        os.remove(file_path)


    return allScore

def getStudentScore(id, passwd):
    allScore = {}
    isContinue = True
    while (isContinue):
        try:
            allScore = get_selenium(id, passwd,"https://portal.dju.ac.kr/index.jsp")
            break

        except UnexpectedAlertPresentException:
            print("95%확률로 아이디 또는 비번 오류!")
            isContinue = False

        except InvalidSessionIdException:
            print("너무 많이 실행함")
            isContinue = False

        except NoSuchWindowException:
            print("창이 없다고 한다...")
            isContinue = False

        except TimeoutException:
            print("시간초과 오류(점검페이지)")
            isContinue = False

        except Exception as e:
            print(f"예외(module.getScore) : {str({e})}")
            print()
        finally:
            pass
    return allScore
