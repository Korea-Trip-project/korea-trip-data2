import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Buttons to use callbacks
button_code = '''        if st.button("🗺️ 전체 선택", use_container_width=True, key="btn_sel_all_new"):
            for c_name in country_options.keys():
                st.session_state[f"chk_{c_name}"] = True
            st.rerun()
            
        if st.button("❌ 전체 해제", use_container_width=True, key="btn_desel_all_new"):
            for c_name in country_options.keys():
                st.session_state[f"chk_{c_name}"] = False
            st.session_state["chk_전세계 (Global)"] = True
            st.rerun()'''

new_button_code = '''        def select_all_cb():
            for c_name in country_options.keys():
                st.session_state[f"chk_{c_name}"] = True

        def deselect_all_cb():
            for c_name in country_options.keys():
                st.session_state[f"chk_{c_name}"] = False
            st.session_state["chk_전세계 (Global)"] = True

        st.button("🗺️ 전체 선택", use_container_width=True, key="btn_sel_all_new", on_click=select_all_cb)
        st.button("❌ 전체 해제", use_container_width=True, key="btn_desel_all_new", on_click=deselect_all_cb)'''

if button_code in content:
    content = content.replace(button_code, new_button_code)
else:
    print("Warning: Button code not found. Trying flexible regex.")
    content = re.sub(r'if st\.button\("🗺️ 전체 선택".*?st\.rerun\(\)', new_button_code, content, flags=re.DOTALL)

# 2. Add New CSS
new_css = '''
/* --- STICKY MENU (Excel Freeze Pane Style) --- */
header[data-testid="stHeader"] {
    background: transparent !important;
    height: 0 !important;
}
div.block-container {
    padding-top: 150px !important;
}
div.custom-main-title {
    position: fixed !important;
    top: 15px !important;
    left: 3rem !important;
    z-index: 999999 !important;
    background-color: rgba(15, 23, 42, 0.95) !important;
    padding: 10px 20px !important;
    border-radius: 8px !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(255,255,255,0.05);
}
div[data-testid="stVerticalBlock"] > div:nth-child(1) div[data-testid="stRadio"] {
    position: fixed !important;
    top: 20px !important;
    right: 3rem !important;
    z-index: 999999 !important;
}
div[data-testid="stTabs"] > div[data-baseweb="tab-list"] {
    position: fixed !important;
    top: 80px !important;
    left: 0 !important;
    width: 100vw !important;
    z-index: 999999 !important;
    background-color: rgba(15, 23, 42, 0.95) !important;
    padding: 0 3rem !important;
    border-bottom: 2px solid #334155 !important;
    backdrop-filter: blur(10px) !important;
}

/* --- TAB MENU HOVER EFFECT --- */
div[data-testid="stTabs"] button[role="tab"]:not([aria-selected="true"]):hover {
    background-color: rgba(255, 255, 255, 0.6) !important;
    border-radius: 8px 8px 0 0 !important;
}
div[data-testid="stTabs"] button[role="tab"]:not([aria-selected="true"]):hover p {
    color: #000000 !important;
    font-weight: 700 !important;
}

/* --- RADIO BUTTON STYLING --- */
div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) {
    background-color: rgba(255, 255, 255, 0.6) !important; /* Semi-transparent white */
}
div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) p {
    color: #000000 !important;
    font-weight: 800 !important;
}

/* --- SELECTBOX TEXT CENTER --- */
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:first-child {
    justify-content: center !important;
}
div[data-testid="stSelectbox"] div[data-baseweb="select"] span {
    text-align: center !important;
    width: 100% !important;
    display: inline-block !important;
}
div[data-testid="stSelectbox"] div[class*="ValueContainer"] {
    justify-content: center !important;
    padding: 0 !important;
}
div[data-testid="stSelectbox"] div[class*="singleValue"] {
    text-align: center !important;
    width: 100% !important;
    margin: 0 auto !important;
}
'''

# Remove old radio and selectbox and sticky css to avoid conflicts
# We will just append our new CSS at the very end of the <style> block which will override previous ones because of CSS specificity and order.
content = content.replace('</style>', new_css + '\n</style>', 1)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done!')
