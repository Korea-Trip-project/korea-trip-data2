with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add the Top button markdown safely at the end if it doesn't exist
top_btn_code = """
# 맨 위로 가기 버튼 (플로팅)
st.markdown('<a href="#top" class="top-btn" title="맨 위로 가기">↑</a>', unsafe_allow_html=True)
"""

if 'class="top-btn"' not in content:
    # Ensure it's not inside a block, add it to the very end
    content = content.rstrip() + "\n" + top_btn_code

# Also make sure there is an anchor id="top" at the beginning of the file (after imports)
if '<div id="top"></div>' not in content:
    # Replace the first style tag with the anchor + style tag
    content = content.replace('<style>', '<div id="top"></div>\n<style>', 1)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done fix19!')
