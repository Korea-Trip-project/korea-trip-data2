import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix the CSS for sticky and hover
# Remove .main and section[...] from overflow visible to restore scrolling!
content = content.replace(
    '.main, .block-container, div[data-testid="stVerticalBlock"], div[data-testid="stVerticalBlockBorderWrapper"], section[data-testid="stMain"] {',
    '.block-container, div[data-testid="stVerticalBlock"], div[data-testid="stVerticalBlockBorderWrapper"] {'
)

# Add hover CSS
hover_css = '''
div[data-testid="stTabs"] > div[data-baseweb="tab-list"] button[data-baseweb="tab"]:hover {
    background-color: #FFFFFF !important;
}
div[data-testid="stTabs"] > div[data-baseweb="tab-list"] button[data-baseweb="tab"]:hover p {
    color: #000000 !important;
}
'''
if 'button[data-baseweb="tab"]:hover' not in content:
    content = content.replace('</style>', hover_css + '\n</style>')


# 2. Fix layout
old_layout_start = content.find('    # 국가 및 기간 필터를 위한 2열 레이아웃 (국가 선택에 가로 공간을 대폭 할당합니다)')
old_layout_end = content.find('    with st.spinner("📊 구글 트렌드 국가별 도시 선호도 데이터 수집 및 분석 중..."):')

if old_layout_start != -1 and old_layout_end != -1:
    new_layout = '''    st.markdown("<hr style='margin: 15px 0; border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    col_filter1, col_filter2 = st.columns([8, 2])
    
    with col_filter1:
        st.markdown("<p style='color: #60A5FA; font-size: 0.88rem; font-weight: 700; margin-bottom: 10px;'>🗺️ 비교 분석 대상 국가 선택</p>", unsafe_allow_html=True)
        # 각 국가 체크박스의 세션 기본값 True로 설정
        for c_name in country_options.keys():
            chk_key = f"chk_{c_name}"
            if chk_key not in st.session_state:
                st.session_state[chk_key] = True
                
        # 6열 그리드로 국가 체크박스 나열
        cols = st.columns(6)
        for idx, c_name in enumerate(country_options.keys()):
            with cols[idx % 6]:
                st.checkbox(c_name, key=f"chk_{c_name}")
                
        selected_countries = [c_name for c_name in country_options.keys() if st.session_state.get(f"chk_{c_name}", False)]
        if not selected_countries:
            selected_countries = ["전세계 (Global)"]
            
        selected_country_name = selected_countries[0]
        target_country = country_options[selected_country_name]
        
    with col_filter2:
        timeframe_options = {
            "최근 3개월 (today 3-m)": "today 3-m",
            "최근 12개월 (today 12-m)": "today 12-m"
        }
        # label_visibility를 collapsed로 설정하여 위에 빈 공간을 없앱니다.
        selected_timeframe_name = st.selectbox("분석 대상 기간 선택", list(timeframe_options.keys()), index=0, label_visibility="collapsed")
        target_timeframe = timeframe_options[selected_timeframe_name]
        
        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
        if st.button("🗺️ 전체 선택", use_container_width=True, key="btn_sel_all_new"):
            for c_name in country_options.keys():
                st.session_state[f"chk_{c_name}"] = True
            st.rerun()
            
        if st.button("❌ 전체 해제", use_container_width=True, key="btn_desel_all_new"):
            for c_name in country_options.keys():
                st.session_state[f"chk_{c_name}"] = False
            st.session_state["chk_전세계 (Global)"] = True
            st.rerun()
            
    st.markdown("<hr style='margin: 15px 0 25px 0; border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    
'''
    content = content[:old_layout_start] + new_layout + content[old_layout_end:]

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done!')
