import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the specific hr tag above the comparison country selection
hr_pattern = re.compile(r'st\.markdown\("<hr style=\'margin: 15px 0; border-color: rgba\(255,255,255,0\.1\);\'><hr>"\s*,\s*unsafe_allow_html=True\)', re.DOTALL)
content = content.replace('st.markdown("<hr style=\'margin: 15px 0; border-color: rgba(255,255,255,0.1);\'>", unsafe_allow_html=True)', '')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done fix22!')
