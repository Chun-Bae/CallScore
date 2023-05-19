from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By

from pandas import  DataFrame
from tabulate import tabulate

from bs4 import BeautifulSoup
import re

import time
from dotenv import load_dotenv
import os 

# load .env
load_dotenv()

sid = os.environ.get('STUDENT_ID')
spassword = os.environ.get('PASSWORD')


global driver

driver = Options()
driver.add_experimental_option("detach", True)  # 브라우저 바로 닫힘 방지
driver.add_experimental_option("excludeSwitches", ["enable-logging"])  # 불필요한 메시지 제거
driver.add_argument('--blink-settings=imagesEnabled=false')
driver.add_argument("window-size=1920x1080")
driver.add_argument('headless')

driver.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")

driver = webdriver.Chrome()



############################################################
def getScore():
    driver.get("https://portal.dju.ac.kr/index.jsp")
    driver.maximize_window()

    #### 포탈 접속 입력 ####
    i_d = driver.find_element(By.CLASS_NAME, "id_input1")
    password = driver.find_element(By.CLASS_NAME, "id_input2")
    i_d.send_keys(sid)
    password.send_keys(spassword)
    password.send_keys(Keys.ENTER)
    ######################
    time.sleep(0.3)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//*[@id='homeLink']")))
    driver.find_element(By.XPATH, "//*[@id='homeLink']").click()
    time.sleep(0.3)

    #### 통합 정보 시스템 접속 ####
    driver.get("https://itics.dju.ac.kr/main.do") # 이걸 사용하면 다른 탭이 거슬림.
    driver.switch_to.window(driver.window_handles[0])

    # driver.switch_to.window(driver.window_handles[-1]) # 이걸 사용하면 빈번히 토큰 오류 생김.
    ############################

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"mainframe_waitwindow")))
    time.sleep(0.3)

    #### 성적 조회 창 접속 ####
    search_keyword = driver.find_element(By.TAG_NAME,"input")
    search_keyword.click()
    search_keyword.send_keys("전체성적조회")
    search_keyword.send_keys(Keys.ENTER)
    time.sleep(0.3)

    driver.find_element(By.ID, "mainframe_childframe_form_leftContentDiv_widType_BTN_SEARCH_MENU_DIV_menuDiv_DG_LEFT_MENU_body_gridrow_1").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"mainframe_childframe_form_mainContentDiv_workDiv_WINB010603_INFODIV01_INFODIV01_Title00")))
    time.sleep(0.3)
    ############################

    with open("crypto.html", "w", encoding="utf8") as f:
        f.write(driver.page_source)
        
    ############################

    soup = BeautifulSoup(driver.page_source, "lxml")
        
    seeing_list = ["classification", "class_num", "subject", "div_class", "credit", "grade", "score", "rating"]
    figure_list = ["req_credit","acq_creidt","rating_cnt","rating_avg","r_scores","r_scores_avg","per_score"]



    for i in range(16):
        seeing = {}    
        ###############성적표 찾기#################      
        for j in range(12):
            try:
                
                finds_text = soup.find_all(id=re.compile('INFODIV01_INFODIV01_DG_GRID{0}_body_gridrow_._cell_._{1}GridCellTextContainerElement'.format(str(i).zfill(2),j)))
                
                seeing['{}'.format(seeing_list[j])] = [find_text.get_text().strip() for find_text in finds_text]
            
            except:
                print("과목 끝")
                break
        ###############학기 이름 찾기#################   
        print(seeing)
        try:
            finds_text = soup.find(id=re.compile('INFODIV01_INFODIV01_Title{}TextBox'.format(str(i).zfill(2)))).get_text().strip().split(" ")
        except:
            print("학기 이름 끝")
            break
        
        
        pattern1 = re.compile("\d\d\d\d")
        pattern2 = re.compile("[^학기정규<>]+")    

        a = pattern1.search(finds_text[0])
        b = pattern2.search(finds_text[1])
        
        a = a.group()
        if b.group() == '겨울':
            b = 'winter'
        elif b.group() == '여름':
            b = 'summer'
        else:
            b = b.group()    
        ###############전체 수치#################
        globals()['sem_{0}_{1}_figure'.format(a,b)] = {}
        
        finds_text = soup.find(id=re.compile('INFODIV01_INFODIV01_Sum{}TextBoxElement'.format(str(i).zfill(2)))).get_text().replace(" ","").split("*")
        finds_text = list(filter(None, finds_text))
        for k in range(len(finds_text)):        
            pattern1 = re.compile("\d+.\d+")
            finds_text[k] = pattern1.search(finds_text[k]).group()    
            globals()['sem_{}_{}_figure'.format(a,b)]['{}'.format(figure_list[k])] = finds_text[k]
        
        print(globals()['sem_{}_{}_figure'.format(a,b)])
        ############### 결과 #################     
        globals()['sem_{0}_{1}'.format(a,b)] = DataFrame(seeing)
        

        print(tabulate(DataFrame(seeing) , headers='keys', tablefmt='psql', showindex=True))

    os.remove('crypto.html') # 해쉬파일로 바꾸기 (배포시 구분용)


# 실행
while(True):
        try:
            getScore()
            break
        except Exception as e:
            print("예외 발생 : " + e)