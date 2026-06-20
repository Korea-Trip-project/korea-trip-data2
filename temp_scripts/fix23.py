import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace multiple newlines and spaces on blank lines with a single newline inside <style> tags
def clean_style(match):
    style_content = match.group(2)
    # Remove all blank lines
    style_content = re.sub(r'\n\s*\n', '\n', style_content)
    return match.group(1) + style_content + match.group(3)

content = re.sub(r'(<style>)(.*?)(</style>)', clean_style, content, flags=re.DOTALL)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done fix23!')
