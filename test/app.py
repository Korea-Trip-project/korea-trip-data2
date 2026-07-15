import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

# -----------------------------------------------------------------------------
# 0. 한글 폰트 설정 (WordCloud 및 Matplotlib용 기본 폰트 설정)
# -----------------------------------------------------------------------------
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

# -----------------------------------------------------------------------------
# 1. 가상 데이터 생성 (서울, 부산, 제도를 제외한 주요 도시 12곳)
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    cities = ["경주", "강릉", "안동", "수원", "양양", "남해", "울산", "평택", "창원", "춘천", "여수", "전주"]
    
    # 가상 데이터 생성
    np.random.seed(42)
    data = {
        "도시": cities,
        # 온라인 관심도 (0~100)
        "온라인_관심도": [92, 88, 75, 80, 85, 70, 30, 25, 35, 78, 83, 89],
        # 실제 방문도 (0~100)
        "실제_방문도": [90, 85, 60, 82, 40, 30, 75, 80, 70, 74, 78, 81],
        # 교통 접근성 점수 (0~100) - KTX, 고속도로 등 편리성
        "교통_접근성": [85, 80, 65, 95, 45, 35, 90, 92, 88, 82, 75, 80],
        # 다국어 인프라 점수 (0~100) - 표지판, 다국어 예약 등
        "다국어_인프라": [88, 78, 70, 85, 50, 40, 60, 55, 50, 75, 70, 82],
        # 주요 관심사 (WordCloud용)
        "관심_키워드": [
            "역사 템플스테이 불국사 한옥 문화재 첨성대 전통",
            "바다 서핑 카페거리 해변 순두부 힐링 동해",
            "하회탈 전통 한옥 고택 역사 서원 안동찜닭",
            "수원화성 성곽 갈비 당일치기 역사 근교 지하철",
            "서핑 양양 서피비치 클럽 젊음 바다 인스타",
            "독일마을 다랭이마을 남해대교 힐링 바다 드라이브",
            "비즈니스 출장 공업 공장 바이어 현대 산업",
            "미군기지 비즈니스 산업단지 평택항 일자리 근로자",
            "산업 비즈니스 출장 창원공단 벚꽃 군항제 기계",
            "닭갈비 남이섬 호수 엠티 가평 근교 ITX",
            "여수밤바다 낭만포차 돌산대교 케이블카 간장게장",
            "한옥마을 먹방 전주비빔밥 막걸리 한복 성당"
        ],
        # 방문 목적 비율
        "관광_비율": [85, 90, 80, 70, 95, 90, 15, 10, 20, 85, 88, 85],
        "비즈니스_비율": [5, 3, 10, 20, 2, 2, 75, 80, 70, 5, 5, 5],
        "기타_비율": [10, 7, 10, 10, 3, 8, 10, 10, 10, 10, 7, 10]
    }
    df = pd.DataFrame(data)
    
    # 사분면 정의
    # 관심도 평균, 방문도 평균을 기준으로 분류
    x_mean = df["온라인_관심도"].mean()
    y_mean = df["실제_방문도"].mean()
    
    def classify_quadrant(row):
        if row["온라인_관심도"] >= x_mean and row["실제_방문도"] >= y_mean:
            return "1사분면 (Superstars)"
        elif row["온라인_관심도"] < x_mean and row["실제_방문도"] >= y_mean:
            return "2사분면 (Hidden Gems)"
        elif row["온라인_관심도"] < x_mean and row["실제_방문도"] < y_mean:
            return "3사분면 (Low Priority)"
        else:
            return "4사분면 (Wishlist Cities)"
            
    df["사분면"] = df.apply(classify_quadrant, axis=1)
    return df, x_mean, y_mean

df, x_mean, y_mean = load_data()

# -----------------------------------------------------------------------------
# 2. 대시보드 레이아웃 설정
# -----------------------------------------------------------------------------
st.set_page_config(page_title="한국 로컬 도시 분석", layout="wide")

st.title(" 한국 로컬 도시 외국인 관심도-방문도 분석")
st.markdown("##### 서울, 부산, 제도를 제외한 우리나라 주요 도시들에 대한 외국인들의 온라인 관심과 실제 오프라인 방문 상관관계를 분석합니다.")
st.write("---")

# 상단 공통 필터
st.sidebar.header(" 글로벌 대시보드 필터")
selected_year = st.sidebar.selectbox("연도 선택", ["2025 (최근 1년)", "2024"])
selected_country = st.sidebar.multiselect("외국인 분석 국가", ["전체", "영어권", "중화권", "일본", "동남아"], default="전체")

# 메인 탭(메뉴) 구성
tab1, tab2, tab3, tab4 = st.tabs([
    " 1. 온라인 관심도", 
    " 2. 실제 방문도", 
    " 3. 비교 분석 (핵심)", 
    " 4. 개별 도시 심층 탐구"
])

# -----------------------------------------------------------------------------
# Tab 1. 온라인 관심도 분석
# -----------------------------------------------------------------------------
with tab1:
    st.header(" 외국인들은 한국 어떤 도시에 관심이 많을까?")
    st.subheader("온라인 탐색 및 SNS 언급량 지표 분석")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("#### **도시별 온라인 관심도 랭킹 (Top 12)**")
        df_sorted_interest = df.sort_values(by="온라인_관심도", ascending=False)
        fig_interest = px.bar(
            df_sorted_interest, 
            x="도시", 
            y="온라인_관심도", 
            text="온라인_관심도",
            color="온라인_관심도",
            color_continuous_scale="Purples",
            labels={"온라인_관심도": "관심도 점수 (Max 100)"}
        )
        fig_interest.update_traces(texttemplate='%{text}점', textposition='outside')
        fig_interest.update_layout(yaxis=dict(range=[0, 110]))
        st.plotly_chart(fig_interest, use_container_width=True)
        
    with col2:
        st.markdown("#### **1-1. 왜 관심이 많을까? 주요 키워드 분석**")
        selected_city_t1 = st.selectbox("키워드를 확인하고 싶은 도시를 선택하세요:", df["도시"].unique(), key="t1_city")
        
        # 선택한 도시의 관심사 워드클라우드 생성
        text_data = df[df["도시"] == selected_city_t1]["관심_키워드"].values[0]
        
        # 한국어 폰트가 설치되어 있지 않을 때를 대비해 Matplotlib 기본 플롯으로 대체 시각화
        fig, ax = plt.subplots(figsize=(6, 4))
        
        font_path = "C:/Windows/Fonts/malgun.ttf"
        if not os.path.exists(font_path):
            font_path = None
            
        wordcloud = WordCloud(
            width=400, height=300, 
            background_color='white',
            font_path=font_path
        ).generate(text_data)
        
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)
        st.info(f" **{selected_city_t1}**의 인기 태그: {text_data}")

# -----------------------------------------------------------------------------
# Tab 2. 실제 방문도 분석
# -----------------------------------------------------------------------------
with tab2:
    st.header(" 실제로 관심이 많은 지역에 많이 방문했을까?")
    st.subheader("외국인 유동인구 및 카드 소비 기반 오프라인 지표 분석")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("#### **도시별 실제 방문도 랭킹 (Top 12)**")
        df_sorted_visit = df.sort_values(by="실제_방문도", ascending=False)
        fig_visit = px.bar(
            df_sorted_visit, 
            x="도시", 
            y="실제_방문도", 
            text="실제_방문도",
            color="실제_방문도",
            color_continuous_scale="Oranges",
            labels={"실제_방문도": "방문도 점수 (Max 100)"}
        )
        fig_visit.update_traces(texttemplate='%{text}점', textposition='outside')
        st.plotly_chart(fig_visit, use_container_width=True)
        
    with col2:
        st.markdown("#### **2-1. 왜 실제 방문이 많거나 적을까?**")
        st.write("주요 인프라 점수 비교 (교통 편의성 vs 다국어 서비스)")
        
        fig_infra = go.Figure()
        fig_infra.add_trace(go.Bar(
            x=df["도시"], y=df["교통_접근성"],
            name='교통 접근성',
            marker_color='indianred'
        ))
        fig_infra.add_trace(go.Bar(
            x=df["도시"], y=df["다국어_인프라"],
            name='다국어 지원 인프라',
            marker_color='lightsalmon'
        ))
        fig_infra.update_layout(barmode='group', height=350, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig_infra, use_container_width=True)
        st.caption(" 교통 접근성 및 다국어 인프라 수치가 실제 방문을 견인하는 중요한 조절 변수(Modifier)가 됩니다.")

# -----------------------------------------------------------------------------
# Tab 3. 비교 분석 (핵심 사분면)
# -----------------------------------------------------------------------------
with tab3:
    st.header(" 관심도 vs 방문도 비교 분석")
    st.subheader("외국인 인지도와 실제 행동의 미스매칭(Gap) 발굴")
    
    # 4사분면 분산 차트 시각화
    fig_scatter = px.scatter(
        df, 
        x="온라인_관심도", 
        y="실제_방문도", 
        color="사분면",
        text="도시",
        hover_data=["교통_접근성", "다국어_인프라"],
        color_discrete_map={
            "1사분면 (Superstars)": "#2ca02c", # 초록
            "2사분면 (Hidden Gems)": "#ff7f0e", # 주황
            "3사분면 (Low Priority)": "#7f7f7f", # 회색
            "4사분면 (Wishlist Cities)": "#d62728" # 빨강
        },
        title="[관심도 vs 방문도 분산형 맵]",
        labels={"온라인_관심도": "온라인 관심도 (X축)", "실제_방문도": "실제 방문도 (Y축)"}
    )
    
    # 평균 기준선 추가
    fig_scatter.add_vline(x=x_mean, line_dash="dash", line_color="blue", annotation_text=f"관심도 평균 ({x_mean:.1f})")
    fig_scatter.add_hline(y=y_mean, line_dash="dash", line_color="blue", annotation_text=f"방문도 평균 ({y_mean:.1f})")
    fig_scatter.update_traces(textposition='top center', marker=dict(size=12))
    fig_scatter.update_layout(height=550)
    
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # 격차 요인 심층 추론 분석 구역
    st.markdown("---")
    st.markdown("###  주요 격차(Gap) 분석 요인")
    
    gap_col1, gap_col2 = st.columns(2)
    
    with gap_col1:
        st.error(" **3-1. 왜 관심은 많은데 방문이 적을까? (4사분면: Wishlist Cities)**")
        st.markdown("""
        **대표적인 도시:** 양양, 남해 등
        * **교통 정체 및 접근 허들:** 수도권 혹은 대형 국제공항과의 연계 대중교통(KTX, 직통 셔틀 등) 인프라 부재.
        * **다국어 예약 플랫폼 부재:** SNS에서 감성 숙소, 이색 체험으로 관심은 모았으나, 실제 예약 단계에서 한국어 인증이나 결제 수단 한계로 도중에 포기하는 '온라인 예약 이탈률'이 높음.
        * **단기 체류형 콘텐츠 편중:** 당일치기나 뷰 위주의 사진 촬영 장소는 많으나 장기 체류(숙박)를 유인할 인프라가 미흡함.
        """)
        # 4사분면 도시 필터링 및 확인
        wishlist_cities = df[df["사분면"] == "4사분면 (Wishlist Cities)"][["도시", "교통_접근성", "다국어_인프라"]]
        st.dataframe(wishlist_cities.style.background_gradient(cmap="Reds"), use_container_width=True)
        
    with gap_col2:
        st.warning(" **3-2. 왜 관심은 적은데 방문이 많을까? (2사분면: Hidden Gems)**")
        st.markdown("""
        **대표적인 도시:** 울산, 평택, 창원 등
        * **비즈니스 배후 수요:** 관광 목적보다는 국가 산업 단지, 글로벌 대기업 공장, 군사 기지 등의 존재로 외국인 바이어 및 상주 근로자 중심의 비자발적(?) 고정 유입이 많음.
        * **비관광형 데이터의 착시:** 통신사 로밍 데이터는 '관광'과 '출장/이주'를 명확하게 구분하지 못해 실제 여행 콘텐츠의 매력도와는 무관하게 방문 수치가 높게 집계될 수 있음.
        """)
        # 2사분면 도시 필터링 및 확인
        hidden_gems = df[df["사분면"] == "2사분면 (Hidden Gems)"][["도시", "교통_접근성", "다국어_인프라"]]
        st.dataframe(hidden_gems.style.background_gradient(cmap="Oranges"), use_container_width=True)

# -----------------------------------------------------------------------------
# Tab 4. 개별 도시 심층 탐구
# -----------------------------------------------------------------------------
with tab4:
    st.header(" 도시별 상세 지표 심층 탐구")
    st.write("관심 있는 특정 소도시를 선택하여 세부 프로필과 방문 유형을 분석할 수 있습니다.")
    
    selected_city_t4 = st.selectbox("상세 정보를 확인할 도시를 선택하세요:", df["도시"].unique(), key="t4_city")
    
    city_info = df[df["도시"] == selected_city_t4].iloc[0]
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        st.metric(label="온라인 관심도 점수", value=f"{city_info['온라인_관심도']} 점", delta=f"{city_info['온라인_관심도'] - x_mean:.1f} (평균 대비)")
        st.metric(label="교통 접근성 수준", value=f"{city_info['교통_접근성']} 점")
        
    with col2:
        st.metric(label="실제 오프라인 방문도", value=f"{city_info['실제_방문도']} 점", delta=f"{city_info['실제_방문도'] - y_mean:.1f} (평균 대비)")
        st.metric(label="다국어 인프라 수준", value=f"{city_info['다국어_인프라']} 점")
        
    with col3:
        st.markdown(f"#### **{selected_city_t4} 외국인 방문 목적 추정 비율**")
        
        labels = ['관광 목적', '비즈니스 목적', '기타 이주/경유']
        sizes = [city_info['관광_비율'], city_info['비즈니스_비율'], city_info['기타_비율']]
        colors = ['#ff9999', '#66b3ff', '#99ff99']
        
        fig_pie = go.Figure(data=[go.Pie(labels=labels, values=sizes, hole=.3, marker=dict(colors=colors))])
        fig_pie.update_layout(height=280, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")
    st.markdown(f"#### ** {selected_city_t4} 도시의 활성화 제안점**")
    if city_info["사분면"] == "4사분면 (Wishlist Cities)":
        st.success(f"**{selected_city_t4}**는 외국인들에게 아주 매력적인 워너비 관광지입니다! 하지만 **교통 접근성({city_info['교통_접근성']}점)**과 **외국어 결제 환경({city_info['다국어_인프라']}점)** 개선이 시급합니다. 수도권 연계 셔틀버스를 증편하거나 해외 신용카드 결제 및 다국어 지원 온라인 모바일 티켓팅을 개선하면 즉시 실제 방문자로 전환될 잠재력이 높습니다.")
    elif city_info["사분면"] == "2사분면 (Hidden Gems)":
        st.warning(f"**{selected_city_t4}**는 비즈니스 및 고정 방문자가 많은 알짜배기 도시입니다. 하지만 관광지로서의 온라인 인지도({city_info['온라인_관심도']}점)가 낮습니다. 방문한 근로자/바이어들이 주말에 소비할 수 있는 '워케이션 코스'나 산업 유산 투어 등의 맞춤형 콘텐츠를 홍보하는 것을 추천합니다.")
    else:
        st.info(f"**{selected_city_t4}**는 현재 **{city_info['사분면']}** 그룹에 위치해 있습니다. 현재 수치에 기반해 로컬 특화 콘텐츠(키워드: {city_info['관심_키워드']}) 중심의 브랜딩 전략을 일관되게 유지하는 것이 좋습니다.")
