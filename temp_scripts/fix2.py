import re
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 'KOREA TOURISM BIG DATA' title color to white
content = re.sub(r'\.custom-main-title\s*\{[^}]*?color:\s*#[0-9a-fA-F]+;', '.custom-main-title {\n    color: #FFFFFF;', content)

# Replace all remaining mint colors
# #11A8B2, #00A3C4, #00D2C4, #2DD4BF, rgba(0, 210, 196
content = content.replace('#11A8B2', '#3B82F6')
content = content.replace('#00A3C4', '#60A5FA')
content = content.replace('#00D2C4', '#60A5FA')
content = content.replace('#2DD4BF', '#60A5FA')
content = content.replace('rgba(0, 210, 196', 'rgba(96, 165, 250') # #60A5FA is 96, 165, 250

# Enhance sticky tabs logic for Streamlit
# We will ensure overflow visible on parents and use sticky
sticky_fix = '''
/* --- STICKY MENU FIX FOR STREAMLIT --- */
/* Remove overflow clipping on parents */
.main, .block-container, div[data-testid="stVerticalBlock"], div[data-testid="stVerticalBlockBorderWrapper"], section[data-testid="stMain"] {
    overflow: visible !important;
}

div[data-testid="stTabs"] > div[data-baseweb="tab-list"],
div[data-testid="stTabs"] > div[role="tablist"] {
    position: sticky !important;
    top: 40px !important;
    z-index: 99999 !important;
    background-color: #0F172A !important;
    padding-top: 10px !important;
    margin-bottom: 0 !important;
    border-bottom: 3px solid #60A5FA !important;
}
'''
if '/* --- STICKY MENU FIX FOR STREAMLIT --- */' not in content:
    content = content.replace('<style>', '<style>\n' + sticky_fix)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done!')
