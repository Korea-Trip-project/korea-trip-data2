# 웹 스크래핑용 API 정보 제공 프롬프트 템플릿

교보문고와 같이 동적(CSR)으로 데이터를 렌더링하는 웹사이트에서 베스트셀러 정보를 정확하게 수집하기 위해, 브라우저 개발자 도구(F12)의 Network 탭에서 획득한 API 정보를 AI에게 제공하여 크롤러 코드를 제작할 때 사용하는 프롬프트 템플릿입니다.

---

## 📋 프롬프트 작성 양식 (AI 전달용)

아래의 양식을 복사하여 괄호 `(...)` 안의 내용을 채운 뒤 AI에게 전달해 주세요.

```markdown
교보문고 IT도서 베스트셀러 데이터를 수집하는 파이썬 스크립트를 작성해 주세요. 
개발자 도구에서 수집한 API 요청 정보는 다음과 같습니다.

1) HTTP 요청 정보
- Request URL: (예: https://store.kyobobook.co.kr/api/gw/pub/pdt/category/best)
- Request Method: (예: GET)
- 주요 Request Headers:
  User-Agent: (자신의 브라우저 User-Agent)
  Referer: https://store.kyobobook.co.kr/category/domestic/33/best?page=2&per=50
  Accept: application/json, text/plain, */*

2) Payload 정보 (Query String Parameters 또는 Request Body)
- Parameters:
  {
    "page": 2,
    "per": 50,
    "ctgrId": "33"
  }

3) Response (응답 JSON 데이터 구조의 일부)
- 책 1~2개 분량의 샘플 구조만 복사해서 첨부합니다:
  ```json
  (응답 데이터의 일부 JSON을 여기에 붙여넣기 하세요)
  ```

4) 요구사항 및 수집 확인
- 위 API를 호출하여 컴퓨터/IT 카테고리의 1페이지와 2페이지(총 100개 도서) 데이터를 수집하는 코드를 구현해 주세요.
- 수집할 항목: 순위, 도서명, 저자, 출판사, 가격 등
- 수집된 데이터를 Pandas DataFrame으로 가공한 뒤 `kyobobook/kyobo_it_bestseller.csv` 파일로 저장하고, 성공적으로 수집이 완료되었는지 확인하는 출력 코드를 포함해 주세요.
```

---

## 💡 브라우저 개발자 도구(F12)에서 정보 수집하는 방법

1. **대상 페이지 접속**: 크롬 또는 엣지 브라우저에서 교보문고 베스트셀러 페이지(`https://store.kyobobook.co.kr/category/domestic/33/best?page=2&per=50`)에 접속합니다.
2. **개발자 도구 열기**: 키보드의 `F12` 또는 `Ctrl + Shift + I`를 누릅니다.
3. **네트워크 탭 설정**:
   - 상단 메뉴에서 **Network (네트워크)** 탭을 선택합니다.
   - 필터 메뉴에서 **Fetch/XHR**을 선택하여 API 요청만 필터링합니다.
4. **API 요청 발생시키기**: 페이지를 새로고침(`F5`)하거나 하단의 페이지 번호(예: 2페이지)를 클릭합니다.
5. **요청 정보 복사**:
   - Name 목록에 나타나는 항목 중 도서 목록 데이터를 받아오는 요청(예: `best` 또는 `product`로 시작하는 항목)을 클릭합니다.
   - **Headers 탭**: `Request URL`, `Request Method` 및 `Request Headers` 정보를 복사하여 양식의 **1) HTTP 요청 정보**에 채워 넣습니다.
   - **Payload 탭**: 요청에 동반되는 파라미터(`page`, `per`, `ctgrId` 등)를 확인하여 **2) Payload 정보**에 채워 넣습니다.
   - **Preview 또는 Response 탭**: 반환된 JSON 구조 중 책 한두 권의 정보가 포함된 구조 영역을 찾아 복사한 후 **3) Response**에 붙여넣습니다.
