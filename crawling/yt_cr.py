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
from webdriver_manager.chrome import ChromeDriverManager 
#webdriver로 크롬드라이버의 버전을 알맞게 자동적으로 맞춰주는 부분이다
def set_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver


# 크롤링 전 세팅, 크롬드라이버의 경로를 저장해준다
chrome_driver_path = r'C:/Users/psych/work/project-purifier-master/chromedriver.exe'
# 크롤링 URL
# 찾고 싶은 영상 URL을 이 자리에 넣어주면 된다

url_path =''
#url_path = 'https://www.youtube.com/watch?v=JSUYuo-WFgU' 친일파
#url_path = 'https://www.youtube.com/watch?v=cnrzHIx91ao' 독도
#url_path = 'https://www.youtube.com/watch?v=3AkIDQVKXGo' 김연아소치

# 크롤링 반복 횟수
repeat = 103
#(위의 의미는 스크롤이 99번 내려간다는 뜻입니다)
# 이하 댓글작성자(닉네임), 좋아요 개수, 크리에이터하트 여부는 추후 수정때 그냥 삭제했습니다

comment_lst=[]


with Chrome(executable_path = chrome_driver_path) as driver:
    #time.sleep()으로 대기하는 이유: 중간에 페이지 로딩등의 시간이 지연되는 경우, 중단되는 경우가 있다. 그점을 방지하기 위해 3초정도까지 기다려 주는 것
    wait = WebDriverWait(driver, 20)
    driver.get(url_path) # 영상 url
    time.sleep(3)
    
    # 유튜브 실행 시 자동 영상 재생일 경우, 영상 종료되면 바로 다음 영상으로 넘어가게 된다.
    # 이를 방지하기 위해, 유튜브 영상 중지 후 크롤링 진행
    # 여기 있는 find_element_by_class_name는 html에서 element들을 읽어올때 ytp-play-button(플레이버튼)을 찾는다는 의미이다
    if driver.find_element_by_class_name("ytp-play-button").get_attribute('aria-label') == '일시중지(k)':
        driver.find_element_by_class_name("ytp-play-button").click()
    else:
        pass
    
    # 최초 1회 PAGE_DOWN
    wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.PAGE_DOWN)
    time.sleep(3)
    

    # END 반복 실행
    # 실행 횟수 체크, tqdm은 프로세스 진행률 표시
    for item in tqdm(range(repeat)): # END버튼 반복 횟수, 1회당 20개씩 댓글 업데이트 ,send_key는 키보드 키 입력값을 pc에 보내는 것 
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
        time.sleep(1) # END버튼 클릭 이후, 1초 대기 후, 다시 END 버튼 진행
                
    # 크롤링 데이터 수집 진행
   
    # 댓글 작성자 중 확인된 사용자, 공식 아티스트 채널 값은 text로 가져올 시, (공백) 처리됨
   
    # 댓글 가져오기, css selector를 이용해 'content-text'부분. 즉 댓글란의 텍스트를 읽어온다   
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

#pandas(이하 pd)를 통해 데이터프레임 만들어주고, 거기에 파싱해온 댓글들을 이하와 같은 형태로 저장한다
df = pd.DataFrame({
                   '댓글' : comment_lst})
                   
                   # 인덱스 1부터 실행
df.index = df.index+1

# to_csv 저장
df.to_csv(save_path + '유튜브 댓글 크롤링 ' + str((repeat +1) * 20) +'개 크롤링.csv' , encoding='utf-8-sig')

print('save done')