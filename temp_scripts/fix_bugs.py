import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix NameError by moving city_to_ko_radar definition to the top
if 'city_to_ko_radar = {' in content:
    # Extract the block
    start_idx = content.find('            # 레이더 차트 한글 축 정보')
    end_idx = content.find('            # Plotly 고품질 레이더 차트 생성')
    if start_idx != -1 and end_idx != -1:
        dict_block = content[start_idx:end_idx]
        # Remove from old position
        content = content[:start_idx] + content[end_idx:]
        
        # Insert it before the TOP 3 block
        top3_start = content.find('            # 선택한 국가들 기준 한국 관광도시 순위 집계')
        if top3_start != -1:
            content = content[:top3_start] + dict_block + content[top3_start:]

# 2. Fix CSS for Sticky, Radio, and Selectbox
new_css = '''
/* --- STICKY FIX --- */
.block-container, 
div[data-testid="stAppViewBlockContainer"],
div[data-testid="stVerticalBlock"], 
div[data-testid="stVerticalBlockBorderWrapper"], 
div.element-container, 
div[data-testid="stTabs"] {
    overflow: visible !important;
}
div[data-testid="stTabs"] > div[data-baseweb="tab-list"] {
    position: sticky !important;
    top: 40px !important;
    z-index: 999999 !important;
    background-color: #0F172A !important;
    padding-top: 10px !important;
    border-bottom: 3px solid #60A5FA !important;
}
div.custom-main-title {
    position: sticky !important;
    top: 0 !important;
    z-index: 999999 !important;
    background-color: #0F172A !important;
}

/* --- RADIO BUTTON STYLING --- */
div[data-testid="stRadio"] > div[role="radiogroup"] {
    display: inline-flex;
    background: rgba(255,255,255,0.05);
    padding: 4px;
    border-radius: 8px;
    gap: 4px;
}
div[data-testid="stRadio"] label[data-baseweb="radio"] {
    padding: 8px 16px !important;
    border-radius: 6px !important;
    margin: 0 !important;
}
div[data-testid="stRadio"] div[data-baseweb="radio"] > div:first-child {
    display: none !important; /* Hide the radio circle */
}
div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) {
    background-color: #FFFFFF !important;
}
div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) p {
    color: #000000 !important;
    font-weight: 800 !important;
}

/* --- SELECTBOX TEXT CENTER --- */
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:first-child {
    justify-content: center !important;
}
div[data-testid="stSelectbox"] div[class*="singleValue"] {
    text-align: center !important;
    width: 100% !important;
    justify-content: center !important;
}
'''

# Replace old sticky css with new
old_sticky = '.block-container, div[data-testid="stVerticalBlock"], div[data-testid="stVerticalBlockBorderWrapper"], div.element-container, div[data-testid="stTabs"], div[data-testid="stAppViewBlockContainer"] {'
if old_sticky in content:
    idx = content.find(old_sticky)
    # Remove old sticky block up to '}'
    end_idx = content.find('}', idx) + 1
    content = content[:idx] + content[end_idx:]

content = content.replace('</style>', new_css + '\n</style>', 1)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done!')
