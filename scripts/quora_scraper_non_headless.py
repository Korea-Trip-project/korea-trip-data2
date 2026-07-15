import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import pandas as pd
import time
import sys

options = uc.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')

try:
    print("크롬 브라우저를 실행하는 중 (Non-headless)...")
    driver = uc.Chrome(options=options, headless=False, version_main=149)
    
    url = "https://www.quora.com/search?q=korea%20travel"
    print(f"URL 접속 중: {url}")
    driver.get(url)
    time.sleep(8) # Cloudflare 통과 및 로딩 대기
    
    print("스크롤 다운을 실행하여 질문 추가 로드 중...")
    for i in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print(f"스크롤 {i+1}회 실행 완료")
        time.sleep(3)
        
    print("질문 데이터 파싱 중...")
    questions = driver.find_elements(By.CLASS_NAME, "qu-wordBreak--break-word")
    
    question_list = []
    for q in questions:
        text = q.text.strip()
        if text and text.endswith('?'):
            question_list.append({'question': text})
            
    driver.quit()
    
    if question_list:
        df = pd.DataFrame(question_list).drop_duplicates()
        output_file = "quora_questions.csv"
        df.to_csv(output_file, index=False, encoding="utf-8-sig")
        print(f"수집 완료! 저장된 외국인 질문 수: {len(df)}개 -> {output_file}")
    else:
        print("수집된 질문이 없습니다. 웹사이트 로딩이나 클래스명을 확인해주세요.")
        
except Exception as e:
    print(f"에러 발생: {e}")
    try:
        driver.quit()
    except:
        pass
    sys.exit(1)
