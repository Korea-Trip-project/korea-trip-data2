import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Center text in selectbox
css_center = '''div[data-baseweb="select"] span {
    text-align: center !important;
    width: 100% !important;
    display: inline-block !important;
}'''
if 'div[data-baseweb="select"] span' not in content:
    content = content.replace('</style>', css_center + '\n</style>', 1)

# 2 & 3 & 4. Move TOP 3 box up, change ranking to selected_countries, remove city select

# Locate the beginning of the radar chart
radar_start_idx = content.find('            st.markdown("<p style=\'color:#94A3B8; font-size:0.92rem; font-weight:600; margin-bottom:8px;\'>📍 각 국가별 검색 관심도 다차원 비교 (레이더 차트):</p>", unsafe_allow_html=True)')
radar_end_idx = content.find('            # 분석 대상 도시 선택 셀렉터 제공 (기존 지도 클릭을 대체)')

if radar_start_idx != -1 and radar_end_idx != -1:
    part1 = content[:radar_start_idx]
    radar_block = content[radar_start_idx:radar_end_idx]
    
    # Locate after top3 block
    after_top3_idx = content.find('        with col_metrics_right:')
    if after_top3_idx != -1:
        after_top3_block = content[after_top3_idx:]
        
        # Build the new TOP 3 block
        new_top3_block = '''            # 전체 15개 해외 국가 대상 1, 2, 3순위 관심 국가 랭킹 연산 및 표시
            country_rank_list = []
            for c_name in selected_countries:
                if c_name == "전세계 (Global)":
                    continue
                score = country_scores.get(c_name, {}).get(selected_city_en, 0.0)
                country_rank_list.append((c_name, score))
                
            country_rank_list.sort(key=lambda x: x[1], reverse=True)
            top3 = country_rank_list[:3]
            
            medals = ["🥇 1위", "🥈 2위", "🥉 3위"]
            colors = ["#FFD166", "#E2E8F0", "#FF9F1C"]
            
            # HTML 내부에 들여쓰기가 있으면 Markdown 파서가 코드 블록으로 오인하므로 들여쓰기 공백을 제거하여 처리합니다
            top3_html = f"<div style='background: rgba(22, 29, 48, 0.5); padding: 12px 16px; border-radius: 12px; border: 1px solid rgba(96, 165, 250, 0.2); margin-bottom: 25px;'>" \\
                        f"<p style='color: #60A5FA; font-size: 0.88rem; font-weight: 700; margin: 0 0 10px 0;'>🌍 '{selected_city_ko}' 선호도 최상위 해외 국가 TOP 3</p>" \\
                        f"<div style='display: flex; gap: 8px; justify-content: space-between;'>"
            for i, (c_name, score) in enumerate(top3):
                medal = medals[i]
                color = colors[i]
                c_display_name = c_name.split(" ")[0]
                top3_html += f"<div style='flex: 1; text-align: center; background: rgba(255, 255, 255, 0.02); padding: 6px 4px; border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.04);'>" \\
                             f"<span style='font-size: 0.78rem; color: {color}; font-weight: 700; display: block;'>{medal}</span>" \\
                             f"<span style='font-size: 0.92rem; color: #E2E8F0; font-weight: 800; display: block; margin-top: 2px;'>{c_display_name}</span>" \\
                             f"<span style='font-size: 0.78rem; color: #94A3B8; display: block; margin-top: 2px;'>{score:.1f}점</span>" \\
                             f"</div>"
            top3_html += "</div></div>"
            st.markdown(top3_html, unsafe_allow_html=True)
            
'''
        
        new_content = part1 + new_top3_block + radar_block + after_top3_block
        
        with open('app.py', 'w', encoding='utf-8') as f:
            f.write(new_content)
        print('Done!')
