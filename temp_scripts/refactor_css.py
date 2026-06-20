import re

def update_css():
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. First style block: Global styles
    content = re.sub(r'\.main \{\s*background:.*?;', '.main {\n            background: #0F172A;', content)
    content = re.sub(r'background: rgba\(255, 255, 255, 0\.95\);', 'background: rgba(30, 41, 59, 0.95);\n            color: #F8FAFC;', content)
    content = re.sub(r'border: 1px solid rgba\(0, 0, 0, 0\.05\);', 'border: 1px solid rgba(255, 255, 255, 0.1);', content)
    content = re.sub(r'box-shadow: 0 4px 15px 0 rgba\(0, 0, 0, 0\.05\);', 'box-shadow: 0 4px 15px 0 rgba(0, 0, 0, 0.5);', content)
    content = re.sub(r'color: #475569;', 'color: #CBD5E1;', content)

    # 2. Second style block: Custom header and sticky tabs
    # Replace stApp background
    content = re.sub(r'\.stApp \{\s*background-color: #F8FAFC !important;\s*\}', '.stApp {\n    background-color: #0F172A !important;\n}', content)
    
    # Fix sticky tabs
    # We want to make the tab-list sticky, not the whole stTabs wrapper if it doesn't work, but actually in Streamlit, 
    # to make the tab menu sticky, we target `div[data-testid="stTabs"] [data-baseweb="tab-list"]` or the existing CSS.
    # The existing CSS was:
    # div[data-testid="stTabs"] {
    #     position: sticky;
    #     top: 40px;
    #     z-index: 999;
    #     background-color: #F8FAFC; 
    #     padding-top: 10px;
    # }
    
    # We replace that entire block to properly target the tab-list itself so it stays sticky without scrolling the content inside
    sticky_css_old = r'div\[data-testid="stTabs"\] \{(.*?)\}'
    sticky_css_new = r'''
/* Make only the tab list sticky, not the whole panel container */
div[data-testid="stTabs"] > div[data-baseweb="tab-list"],
div[data-testid="stTabs"] > div[role="tablist"] {
    position: sticky !important;
    top: 40px !important;
    z-index: 999 !important;
    background-color: #0F172A !important;
    padding-top: 10px !important;
    margin-bottom: 0 !important;
    border-bottom: 3px solid #00D2C4 !important;
}

div[data-testid="stTabs"] {
    /* removing old sticky wrapper css */
}
'''
    # We'll replace it using a more targeted replace
    content = re.sub(r'div\[data-testid="stTabs"\] \{\s*position: sticky;[\s\S]*?padding-top: 10px;\s*\}', 
                     sticky_css_new.strip(), content)

    # Inactive tabs styling
    content = re.sub(r'background-color: #E2E8F0 !important;', 'background-color: #1E293B !important;', content)
    content = re.sub(r'color: #64748B !important;', 'color: #94A3B8 !important;', content)
    
    # Active tab styling
    content = re.sub(r'background-color: #CBD5E1 !important;', 'background-color: #334155 !important;', content)
    content = re.sub(r'color: #334155 !important;', 'color: #FFFFFF !important;', content)
    
    # Active tab selected
    content = re.sub(r'background-color: #00A3C4 !important;', 'background-color: #00D2C4 !important;', content)
    
    # Some other hardcoded colors
    content = re.sub(r'color: #3B82F6;', 'color: #60A5FA;', content) # Lighten blue
    content = re.sub(r'color: #00A3C4;', 'color: #00D2C4;', content)
    content = re.sub(r'border-bottom: 3px solid #00A3C4 !important;', 'border-bottom: 3px solid #00D2C4 !important;', content)

    # Let's fix another case where `stTabs` background-color was set:
    content = content.replace('background-color: #F8FAFC;', 'background-color: #0F172A;')

    # Replace inline html color elements
    content = content.replace("color: #475569", "color: #CBD5E1")
    content = content.replace("color: #3B82F6", "color: #60A5FA")
    content = content.replace("background-color: #f8fafc", "background-color: #1E293B") # radio button container
    content = content.replace("border: 1px solid #e2e8f0", "border: 1px solid #334155") # radio button container border
    content = content.replace("background-color: #ffffff !important", "background-color: #334155 !important") # checked radio button
    content = content.replace("color: #0F766E", "color: #2DD4BF") # text inside checked radio
    
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("app.py successfully updated with dark mode and sticky header fixes.")

update_css()

# Write config.toml
import os
os.makedirs('.streamlit', exist_ok=True)
with open('.streamlit/config.toml', 'w', encoding='utf-8') as f:
    f.write('''[theme]
base = "dark"
primaryColor = "#00D2C4"
backgroundColor = "#0F172A"
secondaryBackgroundColor = "#1E293B"
textColor = "#F8FAFC"
font = "sans serif"

[server]
fileWatcherType = "none"
''')
    print("config.toml updated.")
