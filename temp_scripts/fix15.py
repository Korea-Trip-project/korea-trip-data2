with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

end_style = content.find('</style>')

scrollbar_css = '''
/* ========================================================= */
/* --- MAIN SCROLLBAR CONSTRAINED BELOW MENU ---             */
/* ========================================================= */
/* Target the main scrolling containers */
.stAppViewMain::-webkit-scrollbar,
div[data-testid="stAppViewMain"]::-webkit-scrollbar,
html::-webkit-scrollbar,
body::-webkit-scrollbar {
    width: 14px;
}

.stAppViewMain::-webkit-scrollbar-track,
div[data-testid="stAppViewMain"]::-webkit-scrollbar-track,
html::-webkit-scrollbar-track,
body::-webkit-scrollbar-track {
    background: transparent !important;
    margin-top: 115px !important; /* Constrains scrollbar track to below the header */
}

.stAppViewMain::-webkit-scrollbar-thumb,
div[data-testid="stAppViewMain"]::-webkit-scrollbar-thumb,
html::-webkit-scrollbar-thumb,
body::-webkit-scrollbar-thumb {
    background-color: rgba(148, 163, 184, 0.4);
    border-radius: 10px;
    border: 4px solid #0F172A; /* Match the body background so it looks floating */
    background-clip: padding-box;
}

.stAppViewMain::-webkit-scrollbar-thumb:hover,
div[data-testid="stAppViewMain"]::-webkit-scrollbar-thumb:hover,
html::-webkit-scrollbar-thumb:hover,
body::-webkit-scrollbar-thumb:hover {
    background-color: rgba(148, 163, 184, 0.8);
}
'''

if 'MAIN SCROLLBAR CONSTRAINED' not in content:
    new_content = content[:end_style] + scrollbar_css + content[end_style:]
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('Scrollbar CSS added!')
else:
    print('Scrollbar CSS already exists.')
