import re

file_path = r'c:\Users\Rei EA Jo\Downloads\korea trip data\app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Modify the KPI Box HTML
kpi_box_old = """<div style='background: rgba(22, 29, 48, 0.5); padding: 20px; border-radius: 16px; border: 1px solid rgba(0, 210, 196, 0.15); box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.35); backdrop-filter: blur(8px); margin-bottom: 20px; margin-left: 10px;'>
            <h4 style='color: #00D2C4; font-weight: 800; font-size: 1.1rem; margin-top: 0; margin-bottom: 5px;'>📍 [{selected_city_ko}] 핵심 관광 지표 ({rank_label})</h4>
            <p style='color: #94A3B8; font-size: 0.85rem; margin-bottom: 15px;'>지도에서 선택된 <b>{selected_city_ko} ({selected_city_en})</b> 지역의 외국인 관광 수요 및 지수입니다.</p>
            <style>
            .sq-btn {
                background: rgba(17, 24, 39, 0.7); 
                border-radius: 16px; 
                display: flex; 
                flex-direction: column; 
                justify-content: center; 
                align-items: center; 
                text-align: center; 
                box-shadow: 0 4px 12px rgba(0,0,0,0.3); 
                cursor: pointer; 
                transition: all 0.2s ease-in-out;
                padding: 15px 5px;
            }
            .sq-btn:hover {
                transform: translateY(-5px);
                background: rgba(22, 29, 48, 1);
                box-shadow: 0 8px 20px rgba(0,0,0,0.5);
            }
            </style>
            <div style='display: flex; gap: 10px; flex-wrap: wrap; justify-content: flex-start; padding: 5px 0;'>
                <div class='sq-btn' style='border: 1px solid rgba(0, 210, 196, 0.4); flex: 1 1 120px;'>
                    <span style='color: #94A3B8; font-size: 0.75rem; font-weight:600; line-height: 1.4;'>📊 평균 관광<br>다양성 지수</span>
                    <h3 style='color: #00D2C4; font-weight:900; font-size: 1.4rem; margin: 10px 0 0 0;'>{sel_avg_div:.1f}</h3>
                </div>
                <div class='sq-btn' style='border: 1px solid rgba(255, 117, 143, 0.4); flex: 1 1 120px;'>
                    <span style='color: #94A3B8; font-size: 0.75rem; font-weight:600; line-height: 1.4;'>📱 SNS 관광<br>관심도 (언급)</span>
                    <h3 style='color: #FF758F; font-weight:900; font-size: 1.3rem; margin: 10px 0 0 0;'>{sel_sns_val/10000:.1f}만</h3>
                </div>
                <div class='sq-btn' style='border: 1px solid rgba(255, 209, 102, 0.4); flex: 1 1 120px;'>
                    <span style='color: #94A3B8; font-size: 0.75rem; font-weight:600; line-height: 1.4;'>🌍 국제적 관광<br>매력도 지수</span>
                    <h3 style='color: #FFD166; font-weight:900; font-size: 1.4rem; margin: 10px 0 0 0;'>{sel_attract_score:.1f}</h3>
                </div>
                <div class='sq-btn' style='border: 1px solid rgba(0, 119, 255, 0.4); flex: 1 1 120px;'>
                    <span style='color: #94A3B8; font-size: 0.75rem; font-weight:600; line-height: 1.4;'>💳 추정 관광<br>소비 규모</span>
                    <h3 style='color: #0077FF; font-weight:900; font-size: 1.3rem; margin: 10px 0 0 0;'>{sel_consume_val/1000000:,.0f}백만</h3>
                </div>
            </div>
            </div>"""

kpi_box_new = """<div style='background: rgba(255, 255, 255, 1); padding: 10px; border-radius: 16px; border: 1px solid rgba(0, 210, 196, 0.15); box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1); backdrop-filter: blur(8px); margin-bottom: 20px; margin-left: 10px;'>
            <h4 style='color: #00D2C4; font-weight: 800; font-size: 1.1rem; margin-top: 0; margin-bottom: 5px;'>📍 [{selected_city_ko}] 핵심 관광 지표 ({rank_label})</h4>
            <p style='color: #64748B; font-size: 0.85rem; margin-bottom: 5px;'>지도에서 선택된 <b>{selected_city_ko} ({selected_city_en})</b> 지역의 외국인 관광 수요 및 지수입니다.</p>
            <style>
            .sq-btn {
                background: rgba(248, 250, 252, 1); 
                border-radius: 12px; 
                display: flex; 
                flex-direction: column; 
                justify-content: center; 
                align-items: center; 
                text-align: center; 
                box-shadow: 0 2px 6px rgba(0,0,0,0.05); 
                cursor: pointer; 
                transition: all 0.2s ease-in-out;
                padding: 8px 5px;
            }
            .sq-btn:hover {
                transform: translateY(-2px);
                background: rgba(255, 255, 255, 1);
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }
            </style>
            <div style='display: flex; gap: 10px; flex-wrap: wrap; justify-content: flex-start; padding: 0;'>
                <div class='sq-btn' style='border: 1px solid rgba(0, 210, 196, 0.4); flex: 1 1 120px;'>
                    <span style='color: #475569; font-size: 0.7rem; font-weight:600; line-height: 1.2;'>📊 평균 관광<br>다양성 지수</span>
                    <h3 style='color: #00D2C4; font-weight:900; font-size: 1.1rem; margin: 5px 0 0 0;'>{sel_avg_div:.1f}</h3>
                </div>
                <div class='sq-btn' style='border: 1px solid rgba(255, 117, 143, 0.4); flex: 1 1 120px;'>
                    <span style='color: #475569; font-size: 0.7rem; font-weight:600; line-height: 1.2;'>📱 SNS 관광<br>관심도 (언급)</span>
                    <h3 style='color: #FF758F; font-weight:900; font-size: 1.1rem; margin: 5px 0 0 0;'>{sel_sns_val/10000:.1f}만</h3>
                </div>
                <div class='sq-btn' style='border: 1px solid rgba(255, 209, 102, 0.4); flex: 1 1 120px;'>
                    <span style='color: #475569; font-size: 0.7rem; font-weight:600; line-height: 1.2;'>🌍 국제적 관광<br>매력도 지수</span>
                    <h3 style='color: #FFD166; font-weight:900; font-size: 1.1rem; margin: 5px 0 0 0;'>{sel_attract_score:.1f}</h3>
                </div>
                <div class='sq-btn' style='border: 1px solid rgba(0, 119, 255, 0.4); flex: 1 1 120px;'>
                    <span style='color: #475569; font-size: 0.7rem; font-weight:600; line-height: 1.2;'>💳 추정 관광<br>소비 규모</span>
                    <h3 style='color: #0077FF; font-weight:900; font-size: 1.1rem; margin: 5px 0 0 0;'>{sel_consume_val/1000000:,.0f}백만</h3>
                </div>
            </div>
            </div>"""

if kpi_box_old in content:
    content = content.replace(kpi_box_old, kpi_box_new)
else:
    print("KPI old box not found. Make sure the string matches perfectly.")

# 2. Reorganize the sections
# We need to extract the 5 sections and put them in a menu.
# Let's find the start of section 1
start_1 = content.find("            st.markdown(f\"<h3 style='font-size: 1.2rem; color: #00D2C4; font-weight: 700; margin: 0; padding-left: 10px;'>[{selected_city_ko}] 다차원 지표 분석</h3>\", unsafe_allow_html=True)")
end_1 = content.find("            st.markdown(\"<div style='background: rgba(17, 24, 39, 0.5); padding: 15px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.05); margin-top: 15px; margin-left: 10px;'>\", unsafe_allow_html=True)\n            st.markdown(f\"<h4 style='font-size: 0.95rem; color: #E2E8F0; margin-top: 8px; margin-bottom: 15px;'>⚧️ [{selected_country_name}] 연령/성별 다양성 분석</h4>\", unsafe_allow_html=True)")

start_2 = end_1
end_2 = content.find("            st.markdown(\"<div style='background: rgba(17, 24, 39, 0.5); padding: 15px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.05); margin-top: 15px; margin-left: 10px;'>\", unsafe_allow_html=True)\n            st.markdown(f\"<h4 style='font-size: 0.95rem; color: #E2E8F0; margin-top: 0; margin-bottom: 5px;'>🛍️ [{selected_country_name}] 주요 소비 성향 분석</h4>\", unsafe_allow_html=True)")

start_3 = end_2
end_3 = content.find("        st.markdown(\"<br/>\", unsafe_allow_html=True)\n        if is_mock:")

# sns관심도 키워드별 분석 (starts at st.markdown("<br/><hr/><br/>", unsafe_allow_html=True)\n    st.markdown("<h3 style='font-weight: 600; color: #F8FAFC;'>📱 SNS 관광 관심도 키워드별 분석</h3>", unsafe_allow_html=True))
# Wait, sns sections are at indentation 4 spaces! We need to indent them to 12 spaces to be inside the elif block under col_metrics_right.
start_4 = content.find("    # ----------------- SNS 키워드 분석 섹션 병합 -----------------")
end_4 = content.find("    # 하단 전체 키워드 종합 분포 바 차트")

start_5 = end_4
end_5 = content.find("# ==========================================\n# TAB 1: 종합 요약 분석 (Overview)")

if start_1 != -1 and end_1 != -1 and end_2 != -1 and end_3 != -1 and start_4 != -1 and end_4 != -1 and end_5 != -1:
    sec1 = content[start_1:end_1]
    sec2 = content[start_2:end_2]
    sec3 = content[start_3:end_3]
    
    # Sec 4 and 5 need 8 spaces of indentation added because they were at 4 spaces and now need to be at 12 spaces (inside elif). Wait, originally they were at 4 spaces. The elif block will be at 12 spaces. So we add 8 spaces.
    sec4_raw = content[start_4:end_4]
    sec5_raw = content[start_5:end_5]
    
    sec4 = "\n".join(["        " + line if line.strip() else line for line in sec4_raw.split("\n")])
    sec5 = "\n".join(["        " + line if line.strip() else line for line in sec5_raw.split("\n")])

    # Build the new menu code
    menu_code = """
            # --- 메뉴 선택 ---
            analysis_menu = st.selectbox(
                "📈 분석 지표 선택",
                ["다차원 지표분석", "연령/성별 다양성 분석", "주요 소비 성향분석", "sns관심도 키워드별 분석", "관광키워드 관심도 종합분포"]
            )
            
            if analysis_menu == "다차원 지표분석":
""" + sec1.rstrip() + """
            elif analysis_menu == "연령/성별 다양성 분석":
""" + sec2.rstrip() + """
            elif analysis_menu == "주요 소비 성향분석":
""" + sec3.rstrip() + """
            elif analysis_menu == "sns관심도 키워드별 분석":
""" + sec4.rstrip() + """
            elif analysis_menu == "관광키워드 관심도 종합분포":
""" + sec5.rstrip() + "\n\n"

    # Now replace everything from start_1 to end_3, and remove start_4 to end_5.
    new_content = content[:start_1] + menu_code + content[end_3:start_4] + content[end_5:]
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully refactored app.py")
else:
    print("Could not find some sections.")
    print(f"start_1: {start_1}, end_1: {end_1}")
    print(f"start_2: {start_2}, end_2: {end_2}")
    print(f"start_3: {start_3}, end_3: {end_3}")
    print(f"start_4: {start_4}, end_4: {end_4}")
    print(f"start_5: {start_5}, end_5: {end_5}")

