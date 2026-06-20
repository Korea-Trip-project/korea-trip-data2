import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove the footer
footer_pattern = re.compile(r'# 하단 정보 푸터.*?(?:# 맨 위로 가기 버튼 \(플로팅\)|$)', re.DOTALL)
content = footer_pattern.sub('', content)

# 2. Find the second style block and remove sticky/overflow properties that might break scroll
# Specifically, we want to remove `position: sticky !important;` and `overflow-y: hidden !important;`
# in the second <style> block or anywhere really.
content = re.sub(r'position:\s*sticky\s*!important;', '/* position: sticky removed */', content)
content = re.sub(r'overflow-y:\s*hidden\s*!important;', '/* overflow-y: hidden removed */', content)
content = re.sub(r'overflow-x:\s*hidden\s*!important;', '/* overflow-x: hidden removed */', content)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done fix21!')
