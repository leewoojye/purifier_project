import pandas as pd
import time
from tqdm.auto import tqdm
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# webdriver 설치/ 만약 크롬 드라이버 버전이 맞지 않을 경우를 대비하여 나중에 자동 업데이트 가능하게
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager # <<<<여기서 문제 생겼다
def set_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver


# 크롤링 전 세팅
chrome_driver_path = r'C:/Users/psych/work/project-purifier-master/chromedriver.exe'
# 크롤링 URL #일간베스트 링크
url_path = 'https://www.ilbe.com/list/ilbe'

# 크롤링 반복 횟수
repeat = 3

# 댓글
comment_lst=[]

with Chrome(executable_path = chrome_driver_path) as driver:
    # 찾으려는 대상이 불러올 때까지 지정된 시간만큼 대기하도록 설정한다.
    # 인자는 초(second) 단위이며, Default 값은 0초이다. 
    wait = WebDriverWait(driver, 20)
    driver.get(url_path) # 영상 url
    time.sleep(3)
    
    # 유튜브 실행 시 자동 영상 재생일 경우, 영상 종료되면 바로 다음 영상으로 넘어가게 된다.
    # 이를 방지하기 위해, 유튜브 영상 중지 후 크롤링 진행
    
    
    # 최초 1회 PAGE_DOWN
    wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.PAGE_DOWN)
    time.sleep(3)

    # END 반복 실행
    # 실행 횟수 체크
    for item in tqdm(range(repeat)): # END버튼 반복 횟수, 1회당 20개씩 댓글 업데이트 
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
        time.sleep(1) # END버튼 클릭 이후, 1초 대기 후, 다시 END 버튼 진행
                
    # 크롤링 데이터 수집 진행

    # 댓글 가져오기    
    try:
        for comment in tqdm(wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#content-text')))):
            if comment.text != '':
                comment_temp = comment.text.replace('\n', ' ')
                comment_lst.append(comment_temp)
            else:
                comment_lst.append(' ')            
    except:
        # 크롤링 값이 없을 경우에
        comment_lst.append('')
                
   
print('done')

# 저장 위치
save_path = r'C:/Users/psych/work/project-purifier-master/crawling'


df = pd.DataFrame({ '댓글' : comment_lst})

# 인덱스 1부터 실행
df.index = df.index+1

# to_csv 저장
df.to_csv(save_path + '일베 댓글 크롤링 ' + str((repeat +1) * 20) +'개 크롤링.csv' , encoding='utf-8-sig')

print('save done')
