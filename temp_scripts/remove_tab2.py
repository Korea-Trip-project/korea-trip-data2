import re

file_path = r'c:\Users\Rei EA Jo\Downloads\korea trip data\app.py'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_tabs = """tab_trends, tab1, tab2, tab3, tab5 = st.tabs([
    "📈 실시간 검색 트렌드 (구글트렌드/SNS)",
    "📊 종합 요약 분석 (Overview)", 
    "🌈 관광객 다양성 분석 (Diversity)", 
    "📈 관광 자원 수요 분석 (Demand)", 
    "🗂️ 실시간 연동 데이터 (Raw Data)"
])"""
new_tabs = """tab_trends, tab1, tab3, tab5 = st.tabs([
    "📈 실시간 검색 트렌드 (구글트렌드/SNS)",
    "📊 종합 요약 분석 (Overview)", 
    "📈 관광 자원 수요 분석 (Demand)", 
    "🗂️ 실시간 연동 데이터 (Raw Data)"
])"""
content = content.replace(old_tabs, new_tabs)

pattern = re.compile(r"# ==========================================\n# TAB 2: 관광객 다양성 분석 \(Diversity\)\n# ==========================================\nwith tab2:.*?# ==========================================\n# TAB 3:", re.DOTALL)
content = pattern.sub("# ==========================================\n# TAB 3:", content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Removed Diversity tab.")
