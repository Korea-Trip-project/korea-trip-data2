import re
from datetime import datetime

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Clean up the previous injection from fix12
# Look for the sticky-bg injection block and remove it
injection_pattern = re.compile(r'st\.markdown\(f"""\s*<div class="sticky-bg">.*?</div>\s*""", unsafe_allow_html=True\)', re.DOTALL)
content = injection_pattern.sub('', content)

# 2. Extract the CSS block to replace it
start = content.find('<style>')
end = content.find('</style>')

clean_css = '''
        /* 글로벌 폰트 및 기본 여백 */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Noto+Sans+KR:wght@300;400;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Outfit', 'Noto Sans KR', sans-serif;
        }
        
        /* 메인 백그라운드 */
        .main {
            background: #0F172A;
        }
        
        /* 대시보드 카드 스타일 */
        .metric-card {
            background: #1E293B;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 4px 15px 0 rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            transition: all 0.3s ease;
        }
        .metric-card:hover {
            transform: translateY(-4px);
            border-color: rgba(96, 165, 250, 0.5);
            box-shadow: 0 8px 25px 0 rgba(96, 165, 250, 0.15);
        }
        
        /* 텍스트 타이틀 */
        .gradient-title {
            background: linear-gradient(90deg, #3B82F6 0%, #3B82F6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            font-size: 2.8rem;
            margin-bottom: 0.5rem;
            letter-spacing: -0.05rem;
        }
        
        /* 뱃지 스타일 */
        .badge {
            background-color: rgba(96, 165, 250, 0.15);
            color: #60A5FA;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            border: 1px solid rgba(96, 165, 250, 0.3);
            display: inline-block;
        }
        
        .sub-text {
            color: #94A3B8;
            font-size: 1.05rem;
            margin-bottom: 2rem;
        }

/* ========================================================= */
/* --- SOLID STICKY HEADER (SCROLL PRESERVED) ---            */
/* ========================================================= */
header[data-testid="stHeader"] {
    display: none !important;
}

/* 1. Remove overflow clipping so STICKY works natively */
.block-container,
div[data-testid="stVerticalBlock"],
div[data-testid="stVerticalBlockBorderWrapper"],
div.element-container,
div[data-testid="stTabs"],
div[data-testid="column"] {
    overflow: visible !important;
    clip-path: none !important;
}

/* 2. Sticky Background to hide scrolling content */
div.sticky-bg {
    position: sticky !important;
    top: 0px !important;
    left: 0 !important;
    width: 100vw !important;
    height: 110px !important;
    background-color: #0F172A !important;
    z-index: 999997 !important;
    margin-left: -5rem !important; /* Adjust for default padding */
    margin-bottom: -110px !important; /* Prevent pushing content down */
    pointer-events: none !important;
    border-bottom: 2px solid #334155 !important;
}

/* 3. Sticky Elements */
div.custom-main-title {
    position: sticky !important;
    top: 15px !important;
    z-index: 999999 !important;
    background-color: transparent !important;
    padding: 0 !important;
    margin: 0 !important;
    border: none !important;
}

div[data-testid="stRadio"] {
    position: sticky !important;
    top: 15px !important;
    z-index: 999999 !important;
    background: rgba(255,255,255,0.05);
    padding: 4px;
    border-radius: 8px;
}

/* Tabs Top set to 60px (moved back up to original position) */
div[data-testid="stTabs"] > div:first-child {
    position: sticky !important;
    top: 60px !important;
    z-index: 999999 !important;
    background-color: transparent !important;
    padding: 0 0 !important;
    margin: 0 !important;
    border-bottom: none !important; /* Border handled by background */
}

/* Prevent content hiding behind the fixed header at start */
div.block-container {
    padding-top: 120px !important;
}

/* ========================================================= */
/* --- TAB MENU HOVER EFFECT ---                             */
/* ========================================================= */
div[data-testid="stTabs"] button[role="tab"]:not([aria-selected="true"]):hover {
    background-color: rgba(255, 255, 255, 0.4) !important;
    border-radius: 8px 8px 0 0 !important;
}
div[data-testid="stTabs"] button[role="tab"]:not([aria-selected="true"]):hover p {
    color: #000000 !important;
    font-weight: 500 !important;
}

/* ========================================================= */
/* --- RADIO BUTTON STYLING (Segmented Control) ---          */
/* ========================================================= */
div[data-testid="stRadio"] > div[role="radiogroup"] {
    display: inline-flex;
    gap: 4px;
}
div[data-testid="stRadio"] label[data-baseweb="radio"],
div[data-testid="stRadio"] label {
    padding: 8px 16px !important;
    border-radius: 6px !important;
    margin: 0 !important;
}
div[data-testid="stRadio"] div[data-baseweb="radio"] > div:first-child,
div[data-testid="stRadio"] label > div:first-child {
    display: none !important;
}
/* Selected state: match hover */
div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked),
div[data-testid="stRadio"] label:has(input:checked) {
    background-color: rgba(255, 255, 255, 0.4) !important;
}
div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) p,
div[data-testid="stRadio"] label:has(input:checked) p {
    color: #000000 !important;
    font-weight: 500 !important;
}

/* ========================================================= */
/* --- SELECTBOX TEXT CENTER ---                             */
/* ========================================================= */
div[data-testid="stSelectbox"] div[data-baseweb="select"] {
    position: relative !important;
}
div[data-testid="stSelectbox"] div[class*="-singleValue"],
div[data-testid="stSelectbox"] div[class*="singleValue"] {
    position: absolute !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: auto !important;
    text-align: center !important;
}
'''

new_content = content[:start+7] + '\n' + clean_css + '\n' + content[end:]

# 3. Insert ONLY the sticky-bg right after st.set_page_config
config_end = new_content.find(')', new_content.find('st.set_page_config')) + 1
if config_end > 0:
    injection = '''
st.markdown('<div class="sticky-bg"></div>', unsafe_allow_html=True)
'''
    new_content = new_content[:config_end] + '\n' + injection + new_content[config_end:]

# 4. Insert the footer at the very end of the file
footer_code = '''
# 하단 정보 푸터
st.markdown("---")
from datetime import datetime
st.markdown(f"""
<div style='text-align: center; color: #64748B; font-size: 0.85rem; padding: 20px 0;'>
대한민국 공공데이터포털(data.go.kr) & 한국관광공사 TourAPI 실시간 연동 대시보드<br/>
Designed & Programmed by <b>Antigravity</b> Team. Current System Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
</div>
""", unsafe_allow_html=True)
'''

# Check if footer is already at the end
if '# 하단 정보 푸터' not in new_content[-500:]:
    new_content = new_content + '\n' + footer_code

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(new_content)
print('Done fix13!')
