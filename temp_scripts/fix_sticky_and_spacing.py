import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix sticky menu: add more parent containers to overflow: visible
old_overflow = '.block-container, div[data-testid="stVerticalBlock"], div[data-testid="stVerticalBlockBorderWrapper"] {'
new_overflow = '.block-container, div[data-testid="stVerticalBlock"], div[data-testid="stVerticalBlockBorderWrapper"], div.element-container, div[data-testid="stTabs"], div[data-testid="stAppViewBlockContainer"] {'
content = content.replace(old_overflow, new_overflow)

# 2. Fix 3 boxes spacing: Remove the manual margin-top
margin_div = 'st.markdown("<div style=\'margin-top: 10px;\'></div>", unsafe_allow_html=True)\n'
content = content.replace(margin_div, '')
margin_div2 = 'st.markdown("<div style=\'margin-top: 10px;\'></div>", unsafe_allow_html=True)'
content = content.replace(margin_div2, '')

# Also, sometimes the buttons have no margin bottom, so let's use CSS to ensure uniform gap if needed,
# But removing the manual div is usually enough for Streamlit's default uniform spacing.

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done!')
