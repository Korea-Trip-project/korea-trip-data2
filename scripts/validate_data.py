# -*- coding: utf-8 -*-
import requests
import json
import os
import pandas as pd

results = {}

# ===========================
# 1. Google Trends API
# ===========================
print("=== 1. Google Trends (pytrends) API ===")
try:
    from pytrends.request import TrendReq
    pt = TrendReq(hl='en-US', tz=540, retries=1, backoff_factor=0.5)
    pt.build_payload(['Seoul'], geo='US', timeframe='today 1-m')
    df = pt.interest_over_time()
    if df is not None and not df.empty:
        print(f"[SUCCESS] 실제 데이터 수신: {len(df)}행, 컬럼: {list(df.columns)}")
        results['google_trends'] = 'SUCCESS - 실제 API 데이터'
    else:
        print("[FALLBACK] 빈 응답 -> 모의 데이터로 폴백")
        results['google_trends'] = 'FALLBACK - 빈 응답, 모의 데이터 사용'
except Exception as e:
    print(f"[FALLBACK/ERROR] {e}")
    results['google_trends'] = f'FALLBACK - {type(e).__name__}: {str(e)[:80]}'

print()

# ===========================
# 2. Tripadvisor API
# ===========================
print("=== 2. Tripadvisor Content API ===")
TA_KEY = 'YOUR_TRIPADVISOR_API_KEY'
url = "https://api.content.tripadvisor.com/api/v1/location/search"
try:
    r = requests.get(url, params={"searchQuery": "Seoul", "language": "en", "key": TA_KEY},
                     headers={"accept": "application/json"}, timeout=5)
    code = r.status_code
    print(f"HTTP 상태코드: {code}")
    data_text = r.text[:200]
    print(f"응답: {data_text}")
    if code == 200:
        results['tripadvisor'] = 'SUCCESS - API 정상 동작'
    elif code in [401, 403]:
        results['tripadvisor'] = f'ERROR - API 키 미설정 (HTTP {code}) -> 하드코딩 폴백 사용'
    else:
        results['tripadvisor'] = f'ERROR - HTTP {code} -> 하드코딩 폴백 사용'
except Exception as e:
    results['tripadvisor'] = f'ERROR - {type(e).__name__}: {str(e)[:80]}'
    print(f"[ERROR] {e}")

print()

# ===========================
# 3. 공공데이터포털 API
# ===========================
print("=== 3. 공공데이터포털 API (관광 다양성) ===")
GOV_URLS = {
    '관광다양성': "https://apis.data.go.kr/B551011/AreaTarDivService/areaTouDivList",
    '관광자원수요(서비스)': "https://apis.data.go.kr/B551011/AreaTarResDemService/areaTarSvcDemList",
    '관광자원수요(문화)': "https://apis.data.go.kr/B551011/AreaTarResDemService/areaCulResDemList",
    '방문자수': "https://apis.data.go.kr/B551011/DataLabService/metcoRegnVisitrDDList",
    '연관관광지': "https://apis.data.go.kr/B551011/TarRlteTarService1/areaBasedList1",
}
for name, endpoint in GOV_URLS.items():
    try:
        r = requests.get(endpoint, params={
            'serviceKey': 'INVALID_KEY_FOR_TEST',
            'MobileOS': 'ETC',
            'MobileApp': 'TestApp',
            'baseYm': '202606',
            'areaCd': '11',
            '_type': 'json'
        }, timeout=10)
        code = r.status_code
        body = r.text[:100]
        print(f"  [{name}] HTTP {code}: {body}")
        if code == 200:
            results[f'gov_api_{name}'] = f'HTTP {code} - 키 없이 접근 허용됨 (검증 필요)'
        elif code == 400:
            results[f'gov_api_{name}'] = f'HTTP {code} - 키 오류 (정상적으로 인증 요구)'
        elif code == 500:
            results[f'gov_api_{name}'] = f'HTTP {code} - 잘못된 키로 인한 서버 오류 (정상)'
        else:
            results[f'gov_api_{name}'] = f'HTTP {code}'
    except Exception as e:
        results[f'gov_api_{name}'] = f'ERROR - {str(e)[:60]}'
        print(f"  [{name}] ERROR: {e}")

print()

# ===========================
# 4. GeoJSON 파일 검증
# ===========================
print("=== 4. GeoJSON 파일 검증 ===")
for fname in ['skorea_provinces_geo_simple.json', 'skorea_provinces_geo.json']:
    if os.path.exists(fname):
        try:
            with open(fname, 'r', encoding='utf-8') as f:
                geo = json.load(f)
            features = geo.get('features', [])
            names = [ft.get('properties', {}).get('name', '?') for ft in features[:3]]
            print(f"[OK] {fname}: {len(features)}개 피처, 샘플={names}")
            results[f'geojson_{fname}'] = f'OK - {len(features)}개 행정구역 피처'
        except Exception as e:
            print(f"[ERROR] {fname}: {e}")
            results[f'geojson_{fname}'] = f'ERROR - {e}'
    else:
        print(f"[MISSING] {fname}")
        results[f'geojson_{fname}'] = 'MISSING'

print()

# ===========================
# 5. CSV 파일 검증 (네이버 데이터랩)
# ===========================
print("=== 5. 네이버 데이터랩 CSV 검증 ===")
csv_info = {
    '방문자수': 'extracted_datalab/20260629220728_\ubc29\ubb38\uc790\uc218.csv',
    '관광지출액': 'extracted_datalab/20260629220728_\uad00\uad11\uc9c0\ucd9c\uc561.csv',
    '목적지검색건수': 'extracted_datalab/20260629220728_\ubaa9\uc801\uc9c0\uac80\uc0c9\uac74\uc218.csv',
    'merged_eda': 'extracted_datalab/merged_eda_results.csv',
}
for name, path in csv_info.items():
    if os.path.exists(path):
        try:
            df = pd.read_csv(path)
            nan_total = df.isnull().sum().sum()
            print(f"[OK] {name}: {len(df)}행 x {len(df.columns)}열, NaN={nan_total}")
            results[f'csv_{name}'] = f'OK - {len(df)}행, NaN={nan_total}'
            # 추가 검증
            if name == '방문자수':
                visitor_sum = df['방문자수'].apply(lambda x: float(str(x).replace('E', 'e'))).sum()
                print(f"       전국 방문자 합계: {visitor_sum:,.0f}명")
            elif name == '관광지출액':
                exp_sum = df['관광지출액'].apply(lambda x: float(str(x).replace('E', 'e'))).sum()
                prev_sum = df['전년도 관광지출액'].apply(lambda x: float(str(x).replace('E', 'e'))).sum()
                growth = (exp_sum - prev_sum) / prev_sum * 100
                print(f"       전국 지출액 합계: {exp_sum/1e12:.2f}조원 (YoY +{growth:.2f}%)")
        except Exception as e:
            print(f"[ERROR] {name}: {e}")
            results[f'csv_{name}'] = f'ERROR - {e}'
    else:
        print(f"[MISSING] {name}: {path}")
        results[f'csv_{name}'] = 'MISSING'

print()

# ===========================
# 6. Tumblr CSV 검증
# ===========================
print("=== 6. Tumblr 크롤링 데이터 검증 ===")
tumblr_path = 'tumblr_korea_travel.csv'
if os.path.exists(tumblr_path):
    try:
        df_t = pd.read_csv(tumblr_path)
        print(f"[OK] 포스트 수: {len(df_t)}건")
        print(f"     컬럼: {list(df_t.columns)}")
        print(f"     날짜 범위: {df_t['date'].min()} ~ {df_t['date'].max()}")
        null_body = df_t['body'].isnull().sum()
        null_tags = df_t['tags'].isnull().sum()
        null_title = df_t['title'].isnull().sum()
        print(f"     결측값: body={null_body}, tags={null_tags}, title={null_title}")
        # 태그 다양성
        all_tags = []
        for tags_str in df_t['tags'].dropna():
            if isinstance(tags_str, str):
                all_tags.extend([t.strip().lower() for t in tags_str.split(',') if t.strip()])
        from collections import Counter
        top5 = Counter(all_tags).most_common(5)
        print(f"     상위 5개 태그: {top5}")
        results['tumblr_csv'] = f'OK - {len(df_t)}포스트, body결측={null_body}, tags결측={null_tags}'
    except Exception as e:
        print(f"[ERROR] {e}")
        results['tumblr_csv'] = f'ERROR - {e}'
else:
    print(f"[MISSING] {tumblr_path}")
    results['tumblr_csv'] = 'MISSING'

print()

# ===========================
# 7. Google Translate API (비공식)
# ===========================
print("=== 7. Google Translate API (비공식) 검증 ===")
try:
    r = requests.get("https://translate.googleapis.com/translate_a/single",
                     params={"client": "gtx", "sl": "en", "tl": "ko", "dt": "t", "q": "Korea travel"},
                     timeout=10)
    print(f"HTTP 상태코드: {r.status_code}")
    if r.status_code == 200:
        res = r.json()
        translated = ""
        for item in res[0]:
            if item and item[0]:
                translated += item[0]
        print(f"[SUCCESS] 번역 결과: '{translated}'")
        results['google_translate'] = f'SUCCESS - 정상 동작 ({translated})'
    else:
        results['google_translate'] = f'ERROR - HTTP {r.status_code}'
except Exception as e:
    print(f"[ERROR] {e}")
    results['google_translate'] = f'ERROR - {e}'

print()

# ===========================
# 8. TextBlob 감성분석 모듈
# ===========================
print("=== 8. TextBlob 감성분석 모듈 검증 ===")
try:
    from textblob import TextBlob
    text = "Korea is an amazing country with beautiful nature and delicious food!"
    blob = TextBlob(text)
    pol = blob.sentiment.polarity
    print(f"[SUCCESS] TextBlob 정상: 극성={pol:.3f} ({'긍정' if pol > 0.05 else '중립/부정'})")
    results['textblob'] = f'OK - 극성 분석 정상 (샘플 극성={pol:.3f})'
except ImportError:
    print("[MISSING] TextBlob 미설치 -> 감성분석 비활성화")
    results['textblob'] = 'MISSING - 감성분석 비활성화 (폴백으로 중립 처리)'
except Exception as e:
    print(f"[ERROR] {e}")
    results['textblob'] = f'ERROR - {e}'

print()
print("=== 종합 검증 결과 ===")
for k, v in results.items():
    status = "✅" if v.startswith("OK") or v.startswith("SUCCESS") else ("⚠️" if "FALLBACK" in v else "❌")
    print(f"{status} {k}: {v}")
