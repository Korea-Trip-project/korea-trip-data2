import pandas as pd
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import time
import os

def translate_text(text):
    if not text or not text.strip():
        return text
    try:
        translated = GoogleTranslator(source='en', target='ko').translate(text)
        if translated is None:
            return text
        return translated
    except Exception as e:
        print(f"Translation error: {e}")
        time.sleep(2)
        return text

def translate_html(html_content):
    if not isinstance(html_content, str) or not html_content.strip():
        return html_content
    
    if not ('<' in html_content and '>' in html_content):
        return translate_text(html_content)
        
    soup = BeautifulSoup(html_content, 'html.parser')
    
    import re
    # Find all text strings in HTML and translate them
    for text_node in soup.find_all(string=True):
        parent = text_node.parent
        if parent.name in ['script', 'style']:
            continue
        original_text = str(text_node).strip()
        # 최적화: 영문자가 포함되어 있을 때만 번역 수행
        if original_text and re.search(r'[a-zA-Z]', original_text):
            translated_text = translate_text(original_text)
            if translated_text is not None:
                new_text = str(text_node).replace(original_text, translated_text)
                text_node.replace_with(new_text)
            time.sleep(0.3) # 대기 시간 단축
            
    return str(soup)

def main():
    csv_path = "tumblr_korea_travel.csv"
    if not os.path.exists(csv_path):
        print("CSV file not found!")
        return
        
    print("Reading CSV...")
    df = pd.read_csv(csv_path)
    
    print("Translating titles...")
    titles_ko = []
    for i, title in enumerate(df['title']):
        if pd.isna(title) or not str(title).strip():
            titles_ko.append("")
        else:
            print(f"Translating title {i+1}/{len(df)}: {title}")
            titles_ko.append(translate_text(str(title)))
            time.sleep(0.2)
            
    print("Translating bodies...")
    bodies_ko = []
    for i, body in enumerate(df['body']):
        if pd.isna(body) or not str(body).strip():
            bodies_ko.append("")
        else:
            print(f"Translating body {i+1}/{len(df)}...")
            bodies_ko.append(translate_html(str(body)))
            time.sleep(0.5)
            
    df['title_ko'] = titles_ko
    df['body_ko'] = bodies_ko
    
    # Save the updated CSV
    df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print("Translation completed and saved!")

if __name__ == "__main__":
    main()
