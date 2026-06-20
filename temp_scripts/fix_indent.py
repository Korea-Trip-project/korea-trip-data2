import re

file_path = r'c:\Users\Rei EA Jo\Downloads\korea trip data\app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
in_block = False

for i, line in enumerate(lines):
    # Detect start of our menu block
    if re.match(r'^            if analysis_menu == "다차원 지표분석":\s*$', line):
        in_block = True
        new_lines.append(line)
        continue
    
    # Detect end of the block (the first line after our menu logic)
    if in_block and line.strip() == "st.markdown(\"<br/>\", unsafe_allow_html=True)":
        in_block = False
        new_lines.append(line)
        continue
        
    if in_block:
        # Don't indent the elif statements themselves
        if re.match(r'^            elif analysis_menu == ".*":\s*$', line):
            new_lines.append(line)
        else:
            # Check if line is empty or just whitespace
            if line.strip() == "":
                new_lines.append(line)
            else:
                # Add 4 spaces to the beginning of the line
                new_lines.append("    " + line)
    else:
        new_lines.append(line)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print("Indentation fixed.")
