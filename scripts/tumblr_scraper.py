import os
import sys
import pytumblr
import pandas as pd

# 1. API 키 설정 (환경 변수 또는 직접 입력)
# 발급받은 Consumer Key를 여기에 입력하거나 환경 변수 TUMBLR_CONSUMER_KEY로 설정하세요.
CONSUMER_KEY = os.environ.get('TUMBLR_CONSUMER_KEY', 'wdhOmgV1gXK4hptN0hFf2oL9cpiS9KrB0d1jaNRXq0JkY9fMyK')

if CONSUMER_KEY == 'wdhOmgV1gXK4hptN0hFf2oL9cpiS9KrB0d1jaNRXq0JkY9fMyK' and 'YOUR_CONSUMER_KEY' == 'wdhOmgV1gXK4hptN0hFf2oL9cpiS9KrB0d1jaNRXq0JkY9fMyK':
    # This won't trigger anymore since it's updated
    pass

try:
    # Tumblr 클라이언트 초기화
    client = pytumblr.TumblrRestClient(CONSUMER_KEY)

    # 'korea travel' 태그가 달린 최신 포스트 검색
    print("Tumblr에서 'korea travel' 태그 포스트를 검색하는 중...")
    posts = client.tagged('korea travel')

    # API 응답 결과 검증
    if not isinstance(posts, list):
        print("에러: API 응답이 올바르지 않거나 API 키가 유효하지 않습니다.")
        print(f"응답 결과: {posts}")
        sys.exit(1)

    post_list = []
    for post in posts:
        # 텍스트 타입의 포스트만 정제하여 수집
        if isinstance(post, dict) and post.get('type') == 'text':
            post_list.append({
                'id': post.get('id'),
                'date': post.get('date'),
                'title': post.get('title', ''),
                'body': post.get('body', ''),
                'tags': ", ".join(post.get('tags', [])) # 함께 사용된 태그들
            })

    # 판다스 데이터프레임 변환 후 저장
    if post_list:
        df = pd.DataFrame(post_list)
        output_file = "tumblr_korea_travel.csv"
        df.to_csv(output_file, index=False, encoding="utf-8-sig")
        print(f"수집 완료! 저장된 데이터 수: {len(df)}개 -> {output_file}")
    else:
        print("검색된 텍스트 타입의 포스트가 없습니다.")

except Exception as e:
    print(f"오류가 발생했습니다: {e}")
