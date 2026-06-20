import re
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# The exact old string that was injected multiple times
old_fix = '''
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

# We also need to remove any partial injections if the previous replacement got weird
# But replace is safe enough
content = content.replace('<style>\n' + old_fix, '<style>')
content = content.replace(old_fix, '')

# We will add it ONLY ONCE, and WITHOUT CSS comments to avoid Streamlit Markdown parsing bugs!
clean_fix = '''
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

# Find the very first <style> and inject there
content = content.replace('<style>', '<style>\n' + clean_fix, 1)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed!')
