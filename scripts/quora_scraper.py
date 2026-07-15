from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import sys

# 1. 크롬 드라이버 자동 세팅 및 실행
options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')
options.add_argument('--headless=new') # 헤드리스 모드 활성화 (백그라운드 실행을 위해 필수)
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

try:
    print("크롬 브라우저를 초기화하는 중...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
except Exception as e:
    print(f"브라우저 초기화 실패: {e}")
    sys.exit(1)

try:
    # 2. 쿼라의 한국 여행 검색 결과 페이지로 바로 진입
    url = "https://www.quora.com/search?q=korea%20travel"
    print(f"URL 접속 중: {url}")
    driver.get(url)
    time.sleep(5) # 페이지 로딩 대기

    # 3. 외국인들의 질문을 더 많이 확보하기 위해 아래로 3번 스크롤 내리기
    print("스크롤 다운을 실행하여 질문 추가 로드 중...")
    for i in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print(f"스크롤 {i+1}회 실행 완료")
        time.sleep(3)

    # 4. 질문 제목을 담고 있는 엘리먼트 추출
    print("질문 데이터 파싱 중...")
    questions = driver.find_elements(By.CLASS_NAME, "qu-wordBreak--break-word")

    question_list = []
    for q in questions:
        text = q.text.strip()
        if text and text.endswith('?'): # 질문 형태로 끝나는 문장만 필터링
            question_list.append({'question': text})

    # 5. 브라우저 종료 및 저장
    driver.quit()

    if question_list:
        df = pd.DataFrame(question_list).drop_duplicates() # 중복 제거
        output_file = "quora_questions.csv"
        df.to_csv(output_file, index=False, encoding="utf-8-sig")
        print(f"수집 완료! 저장된 외국인 질문 수: {len(df)}개 -> {output_file}")
    else:
        print("수집된 질문이 없습니다. 웹사이트 로딩이나 클래스명을 확인해주세요.")

except Exception as e:
    print(f"에러 발생: {e}")
    driver.quit()
    sys.exit(1)
