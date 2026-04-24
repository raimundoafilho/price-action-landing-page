#!/usr/bin/env python3
import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent / 'apostila_scraped'
DATA_FILE = BASE_DIR / 'landing-page-data.json'

with open(DATA_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Criar arquivo slim de metadados
metadata = {
    'version': data['version'],
    'createdAt': data['createdAt'],
    'modules': []
}

for module in data.get('modules', []):
    module_meta = {
        'id': module['id'],
        'number': module['number'],
        'title': module['title'],
        'subtitle': module.get('subtitle', ''),
        'topics': []
    }

    for topic in module.get('topics', []):
        module_meta['topics'].append({
            'id': topic['id'],
            'title': topic['title'],
            'slideCount': len(topic.get('slides', []))
        })

    metadata['modules'].append(module_meta)

# Salvar metadados (reduzido)
meta_file = BASE_DIR / 'landing-page-data-meta.json'
with open(meta_file, 'w', encoding='utf-8') as f:
    json.dump(metadata, f, ensure_ascii=False, separators=(',', ':'))

size_meta = os.path.getsize(meta_file)
print(f"[OK] Metadados: {size_meta} bytes")

# Salvar arquivo original comprimido (backup)
import gzip
original_size = os.path.getsize(DATA_FILE)
with open(DATA_FILE, 'rb') as f_in:
    with gzip.open(DATA_FILE + '.gz', 'wb') as f_out:
        f_out.write(f_in.read())

gz_size = os.path.getsize(DATA_FILE + '.gz')
print(f"[OK] Original comprimido: {gz_size} bytes (era {original_size})")
print(f"[OK] Reducao: {original_size - gz_size} bytes")
