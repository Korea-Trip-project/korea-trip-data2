import requests
import json

url = "https://store.kyobobook.co.kr/api/gw/best/v2/best-seller/online"
params = {
    "page": 2,
    "per": 50,
    "saleCmdtClstCode": "33",
    "soldOutExcludeYn": "N",
    "saleCmdtDsplDvsnCode": "KOR",
    "period": "002",
    "dsplDvsnCode": "001",
    "dsplTrgtDvsnCode": "004"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://store.kyobobook.co.kr/category/domestic/33/best?page=2&per=50"
}

try:
    print(f"Sending GET request to {url}...")
    response = requests.get(url, params=params, headers=headers)
    print("Status Code:", response.status_code)
    
    if response.status_code == 200:
        data = response.json()
        print("Success! JSON Keys:", data.keys())
        
        # 데이터의 세부 구조 분석
        # 보통 data['data']['bestSellerList'] 처럼 되어 있을 것입니다.
        # 데이터를 출력하여 정확한 필드명을 파악합니다.
        with open("kyobo_response_sample.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("Saved response to kyobo_response_sample.json")
        
        if "data" in data and "bestSellerList" in data["data"]:
            best_list = data["data"]["bestSellerList"]
            print(f"Found {len(best_list)} items.")
            if best_list:
                print("First item keys:", best_list[0].keys())
                # 필요한 필드 샘플 출력
                item = best_list[0]
                print(f"Rank: {item.get('pureBsttRank') or item.get('rank')}")
                print(f"Title: {item.get('cmdtName')}")
                print(f"Author: {item.get('chtrName')}")
                print(f"Publisher: {item.get('publName')}")
                print(f"Price: {item.get('sapr')}")
        else:
            print("Response struct does not have data -> bestSellerList")
            print(json.dumps(data, indent=2, ensure_ascii=False)[:1000])
    else:
        print("Response Text:", response.text[:1000])
        
except Exception as e:
    print("Error:", e)
