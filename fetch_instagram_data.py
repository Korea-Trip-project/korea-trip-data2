import os
import pandas as pd
from apify_client import ApifyClient

def fetch_data():
    # Load API token from environment variable or local .env file
    APIFY_TOKEN = os.environ.get("APIFY_TOKEN")
    if not APIFY_TOKEN and os.path.exists(".env"):
        with open(".env", "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("APIFY_TOKEN="):
                    APIFY_TOKEN = line.strip().split("=", 1)[1].strip().strip('"').strip("'")
                    break
    
    if not APIFY_TOKEN:
        print("에러: APIFY_TOKEN을 찾을 수 없습니다. .env 파일이나 환경 변수를 확인해 주세요.")
        return False
        
    client = ApifyClient(APIFY_TOKEN)

    hashtags = [
        "gyeongju", "gyeongjutrip", "hanokstay", 
        "gangneung", "yangyang", "koreasurfing", 
        "jeonju", "jeonjuhanokvillage", "koreanfoodtrip",
        "suwon", "suwonhwaseongfortress", "starfieldsuwon"
    ]
    
    # Generate direct URLs for Instagram Hashtags
    direct_urls = [f"https://www.instagram.com/explore/tags/{tag}/" for tag in hashtags]

    actor_id = "apify/instagram-scraper"

    run_input = {
        "directUrls": direct_urls,
        "resultsLimit": 10,              # 태그 한 개당 가져올 포스트 개수 제한 (크레딧 절약 및 빠른 실행을 위해 10개로 설정)
        "resultsType": "posts"
    }

    print(f"총 {len(hashtags)}개의 해시태그에 대한 인스타그램 데이터 수집을 시작합니다...")

    try:
        run = client.actor(actor_id).call(run_input=run_input)
        print(f"Apify Actor 실행 완료. Dataset ID: {run.default_dataset_id}")
        
        dataset_items = client.dataset(run.default_dataset_id).list_items().items
        print(f"수집 완료! 총 {len(dataset_items)}개의 게시물 데이터를 가져왔습니다.")

        if not dataset_items:
            print("수집된 데이터가 없습니다.")
            return False

        df = pd.DataFrame(dataset_items)
        
        # inputUrl에서 hashtag(inputQuery)를 추출하여 매핑
        if 'inputUrl' in df.columns:
            df['inputQuery'] = df['inputUrl'].apply(
                lambda x: str(x).split('/')[-2] if isinstance(x, str) and len(str(x).split('/')) > 2 else ''
            )
        else:
            df['inputQuery'] = ''

        available_columns = df.columns
        target_columns = [
            'inputQuery',       # 검색한 해시태그명
            'id',               # 포스트 고유 ID
            'type',             # 이미지/동영상 구분
            'caption',          # 게시물 본문 텍스트 (외국인 반응 분석 핵심 컬럼)
            'hashtags',         # 함께 사용된 다른 해시태그들
            'likesCount',       # 좋아요 수
            'commentsCount',    # 댓글 수
            'timestamp',        # 작성 시간
            'url'               # 게시물 바로가기 URL
        ]
        
        filtered_columns = [col for col in target_columns if col in available_columns]
        df_final = df[filtered_columns]

        output_filename = "instagram_korea_local_data.csv"
        df_final.to_csv(output_filename, index=False, encoding="utf-8-sig")
        print(f"데이터가 '{output_filename}' 파일로 저장되었습니다.")
        print(df_final.head())
        return True
    except Exception as e:
        print(f"에러가 발생했습니다: {e}")
        return False

if __name__ == "__main__":
    fetch_data()
