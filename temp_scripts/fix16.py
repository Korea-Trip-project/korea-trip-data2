with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

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
/* --- STICKY HEADER (SCROLL PRESERVED NATURALLY) ---        */
/* ========================================================= */
header[data-testid="stHeader"] {
    display: none !important;
}

/* 1. Remove overflow hidden/clip from ALL possible parents of sticky elements! */
/* If any parent clips, sticky fails. */
.block-container,
div[data-testid="stAppViewBlockContainer"],
div[data-testid="stVerticalBlock"],
div[data-testid="stVerticalBlockBorderWrapper"],
div[data-testid="stHorizontalBlock"],
div.element-container,
div[data-testid="stTabs"],
div[data-testid="column"] {
    overflow: visible !important;
    clip-path: none !important;
}

/* 2. Sticky Background */
div.sticky-bg {
    position: sticky !important;
    top: 0px !important;
    left: 0 !important;
    width: 100vw !important;
    height: 115px !important;
    background-color: #0F172A !important;
    z-index: 999997 !important;
    margin-left: -5rem !important; /* Counteract block-container padding */
    margin-bottom: -115px !important; /* Let contents render over it */
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

/* Tabs Top set to 65px */
div[data-testid="stTabs"] > div:first-child {
    position: sticky !important;
    top: 65px !important;
    z-index: 999999 !important;
    background-color: transparent !important;
    padding: 0 !important;
    margin: 0 !important;
    border-bottom: none !important;
}

/* Push rest of content down so it starts below the sticky bg */
div.block-container {
    padding-top: 130px !important;
}

/* ========================================================= */
/* --- MAIN SCROLLBAR CONSTRAINED BELOW MENU ---             */
/* ========================================================= */
/* Target the main scrolling containers */
.stAppViewMain::-webkit-scrollbar,
div[data-testid="stAppViewMain"]::-webkit-scrollbar,
html::-webkit-scrollbar,
body::-webkit-scrollbar {
    width: 14px;
}

.stAppViewMain::-webkit-scrollbar-track,
div[data-testid="stAppViewMain"]::-webkit-scrollbar-track,
html::-webkit-scrollbar-track,
body::-webkit-scrollbar-track {
    background: transparent !important;
    margin-top: 115px !important; /* Constrains scrollbar track to below the header */
}

.stAppViewMain::-webkit-scrollbar-thumb,
div[data-testid="stAppViewMain"]::-webkit-scrollbar-thumb,
html::-webkit-scrollbar-thumb,
body::-webkit-scrollbar-thumb {
    background-color: rgba(148, 163, 184, 0.4);
    border-radius: 10px;
    border: 4px solid #0F172A;
    background-clip: padding-box;
}

.stAppViewMain::-webkit-scrollbar-thumb:hover,
div[data-testid="stAppViewMain"]::-webkit-scrollbar-thumb:hover,
html::-webkit-scrollbar-thumb:hover,
body::-webkit-scrollbar-thumb:hover {
    background-color: rgba(148, 163, 184, 0.8);
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

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(new_content)
print('Done fix16!')
