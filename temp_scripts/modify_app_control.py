import os

filepath = "c:/Users/Rei EA Jo/Downloads/korea trip data/app.py"
with open(filepath, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Replace the old sidebar control panel (from "# ==========================================\n# 3. 사이드바 (CONTROL PANEL)\n" or similar)
# Let's locate the start and end of the sidebar code.
start_str = "# ==========================================\nst.sidebar.markdown(\"<h2 style='color: #00D2C4; font-weight: 800;'>🛠️ CONTROL PANEL</h2>\", unsafe_allow_html=True)"
end_str = "# ==========================================\n# 4. 데이터 로드 및 연동 파트\n# =========================================="

start_idx = code.find(start_str)
end_idx = code.find(end_str)

new_control_panel = """# ==========================================
# 3. CONTROL PANEL (페이지 상단 가로 배치)
# ==========================================
header_container = st.container()

st.markdown("<div style='background: rgba(22, 29, 48, 0.4); padding: 20px 30px; border-radius: 12px; border: 1px solid rgba(0, 210, 196, 0.2); margin-bottom: 25px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);'>", unsafe_allow_html=True)
st.markdown("<h4 style='color: #00D2C4; margin-top: 0; margin-bottom: 20px; font-weight: 800;'>🛠️ CONTROL PANEL</h4>", unsafe_allow_html=True)

col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([1.5, 1.2, 1.3])

with col_ctrl1:
    data_mode = st.radio("데이터 연동 모드", ("데모 데이터 모드 (추천)", "실시간 OpenAPI 연동 모드"), horizontal=True)
    service_key = ""
    if data_mode == "실시간 OpenAPI 연동 모드":
        key_options = {
            "인증키 1": "4a6d8838eb166a4030dde291220ab4516b9502ccdda44a6d8838eb166a4030dd",
            "인증키 2": "ffec4f8bc5da62df9374e291220ab4516b9502ccdda44a6d8838eb166a4030dd",
            "직접 입력": ""
        }
        selected_key_name = st.selectbox("인증키 선택", list(key_options.keys()), index=0)
        if selected_key_name == "직접 입력":
            service_key = st.text_input("공공데이터포털 서비스 키", type="password")
        else:
            service_key = key_options[selected_key_name]
            st.text_input("선택된 서비스 키", value=service_key, type="password", disabled=True)

with col_ctrl2:
    selected_year = st.selectbox("조회 연도", [2025, 2026], index=1)
    selected_month = st.selectbox("조회 월", list(range(1, 13)), index=5)
    base_ym = f"{selected_year}{selected_month:02d}"

with col_ctrl3:
    selected_area_name = st.selectbox("대상 지역 (시/도)", list(AREA_CODES.keys()), index=0)
    selected_area_code = AREA_CODES[selected_area_name]
    target_audience = "외국인 관광객만 보기 (내국인 제외)"
    
    st.markdown(f\"\"\"
        <div style='background: rgba(11, 15, 25, 0.5); padding: 12px; border-radius: 8px; font-size: 0.85rem; color: #94A3B8; margin-top: 10px;'>
            <b style='color: #00D2C4;'>✓ 선택된 조회 정보</b><br/>
            📍 지역: {selected_area_name} ({selected_area_code})<br/>
            📅 기준년월: {selected_year}년 {selected_month}월<br/>
            👥 대상: 외국인 관광객
        </div>
    \"\"\", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

with header_container:
    col_header_1, col_header_2 = st.columns([8, 2])
    with col_header_1:
        st.markdown('<div class="gradient-title">KOREA TOURISM BIG DATA</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sub-text">대한민국 지역별 관광 빅데이터 분석 대시보드 — <b>{selected_area_name} ({base_ym[:4]}년 {base_ym[4:]}월 기준)</b></div>', unsafe_allow_html=True)
    with col_header_2:
        if data_mode == "데모 데이터 모드 (추천)" or not service_key:
            st.markdown('<div style="text-align: right; margin-top: 20px;"><span class="badge" style="background-color: rgba(255, 179, 0, 0.1); color: #FFB300; border-color: rgba(255, 179, 0, 0.2);">📴 DEMO DATA MODE</span></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="text-align: right; margin-top: 20px;"><span class="badge">🌐 REAL-TIME API MODE</span></div>', unsafe_allow_html=True)
    st.markdown("<br/>", unsafe_allow_html=True)

"""

if start_idx != -1 and end_idx != -1:
    code = code[:start_idx] + new_control_panel + code[end_idx:]
else:
    print("Could not find control panel boundaries")

# 2. Remove the old header title block
old_header_start = "# ==========================================\n# 5. 대시보드 UI 구성\n# ==========================================\n\n# 헤더 타이틀 영역\ncol_header_1, col_header_2 = st.columns([8, 2])"
old_header_end = "st.markdown(\"<br/>\", unsafe_allow_html=True)\n\n# ----------------- 탭 구조 정의 -----------------"

oh_start_idx = code.find(old_header_start)
oh_end_idx = code.find(old_header_end)

if oh_start_idx != -1 and oh_end_idx != -1:
    # Remove the header code but keep the UI config start comment
    code = code[:oh_start_idx] + "# ==========================================\n# 5. 대시보드 UI 구성\n# ==========================================\n\n" + code[oh_end_idx:]
else:
    print("Could not find old header boundaries")

# Remove the initial_sidebar_state="expanded" from set_page_config to "collapsed"
code = code.replace('initial_sidebar_state="expanded"', 'initial_sidebar_state="collapsed"')

with open(filepath, "w", encoding="utf-8") as f:
    f.write(code)

print("Modification complete.")
