import json
import re

with open('apostila_scraped/landing-page-data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def clean_content(text):
    text = re.sub(r'\n\d{1,2}\s*$', '', text)
    lines = text.split('\n')
    cleaned = []
    prev = None
    for line in lines:
        if line.strip() and line != prev:
            cleaned.append(line)
            prev = line
    return '\n'.join(cleaned).strip()

for topic in data['topics']:
    for sub in topic['subtopics']:
        sub['content'] = clean_content(sub['content'])

with open('apostila_scraped/landing-page-data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("OK - JSON limpo!")
