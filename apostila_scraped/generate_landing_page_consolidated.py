#!/usr/bin/env python3
"""
GERADOR FINAL: Landing Page JSON - Apostila FIMATHE Price Action
Estrutura consolidada: 5 módulos → tópicos → slides → conteúdo + imagens + tabelas
Data: 2026-04-24
"""

import json
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict

print("\n" + "=" * 80)
print("GERADOR JSON CONSOLIDADO - Landing Page Price Action")
print("=" * 80)

# ============================================================================
# FASE 1: CARREGAR E VALIDAR DADOS BRUTOS
# ============================================================================

print("\n[FASE 1/5] Carregando dados brutos...")

try:
    with open('pdf_extracted.json', 'r', encoding='utf-8') as f:
        pdf_data = json.load(f)
    print(f"  ✓ pdf_extracted.json: {len(pdf_data['pages'])} páginas carregadas")
except Exception as e:
    print(f"  ✗ Erro ao carregar pdf_extracted.json: {e}")
    exit(1)

try:
    with open('pdf_texto_completo.txt', 'r', encoding='utf-8') as f:
        pdf_text_raw = f.read()
    print(f"  ✓ pdf_texto_completo.txt: {len(pdf_text_raw):,} caracteres carregados")
except Exception as e:
    print(f"  ✗ Erro ao carregar pdf_texto_completo.txt: {e}")
    exit(1)

# Parser do texto por página
pages_text = re.split(r'={5,}\nPAGINA\s+(\d+)\n={5,}', pdf_text_raw)
pages_dict = {}

for i in range(1, len(pages_text), 2):
    if i + 1 < len(pages_text):
        try:
            page_num = int(pages_text[i])
            page_content = pages_text[i + 1].strip()
            pages_dict[page_num] = page_content
        except ValueError:
            continue

print(f"  ✓ Texto extraído: {len(pages_dict)} páginas com conteúdo")

# ============================================================================
# FASE 2: IDENTIFICAR ESTRUTURA DE MÓDULOS
# ============================================================================

print("\n[FASE 2/5] Identificando estrutura de módulos...")

# Mapear página → módulo automaticamente
page_to_module = {}
current_module = None

for page_num in range(1, len(pdf_data['pages']) + 1):
    if page_num <= len(pdf_data['pages']):
        page_text = pdf_data['pages'][page_num - 1].get('text', '')

        # Procurar por "Módulo X" no texto
        if 'Módulo' in page_text:
            match = re.search(r'Módulo\s+([^\n]+)', page_text)
            if match:
                current_module = match.group(1).strip()
                page_to_module[page_num] = current_module
        elif current_module:
            page_to_module[page_num] = current_module

# Agrupar páginas por módulo
modules_pages = defaultdict(list)
for page_num, mod_name in page_to_module.items():
    modules_pages[mod_name].append(page_num)

print(f"  ✓ {len(modules_pages)} módulos encontrados:")

# Ordenar módulos por página inicial
modules_sorted = sorted(modules_pages.items(), key=lambda x: min(x[1]))

for idx, (mod_name, pages) in enumerate(modules_sorted, 1):
    page_min, page_max = min(pages), max(pages)
    img_count = sum(len(pdf_data['pages'][p-1].get('images', [])) for p in pages)
    print(f"    {idx}. {mod_name} (páginas {page_min}-{page_max}, {img_count} imagens)")

# ============================================================================
# FASE 3: EXTRAIR TÓPICOS
# ============================================================================

print("\n[FASE 3/5] Extraindo tópicos por módulo...")

modules_with_topics = {}

for mod_name, pages in modules_sorted:
    # Buscar tópicos na primeira página após o início do módulo
    start_page = min(pages) + 1

    topics = []
    if start_page in pages_dict:
        page_content = pages_dict[start_page]
        # Extrair linhas que parecem ser tópicos (linhas curtas, não vazias)
        lines = [l.strip() for l in page_content.split('\n')]
        topics = [
            l for l in lines
            if l and len(l) < 80 and not l.startswith('Licenciado') and l[0].isupper()
        ][:6]  # Máximo 6 tópicos por módulo

    modules_with_topics[mod_name] = {
        'pages': pages,
        'topics': topics if topics else ['Conteúdo Geral']
    }

    print(f"  ✓ {mod_name}:")
    for topic in modules_with_topics[mod_name]['topics']:
        print(f"      • {topic}")

# ============================================================================
# FASE 4: CONSTRUIR ESTRUTURA JSON FINAL
# ============================================================================

print("\n[FASE 4/5] Construindo estrutura JSON consolidada...")

landing_page_data = {
    "metadata": {
        "title": "Método Price Action de Oliver Velez",
        "subtitle": "Mentoria completa com módulos de trading",
        "author": "Oliver Velez",
        "presented_by": "André Trader / FIMATHE",
        "course_type": "Mentoria - Trading Online",
        "difficulty": ["Básico", "Intermediário", "Avançado"],
        "version": "1.0",
        "generated": datetime.now().isoformat(),
        "total_modules": len(modules_sorted),
        "total_topics": sum(len(m['topics']) for m in modules_with_topics.values()),
        "total_slides": len(pdf_data['pages']),
        "total_images": sum(len(p.get('images', [])) for p in pdf_data['pages']),
        "total_tables": sum(len(p.get('tables', [])) for p in pdf_data['pages']),
        "total_pages": len(pdf_data['pages']),
        "language": "pt-BR",
        "license": "Licenciado para - Raimundo Araujo Filho | raimundoaraujo.filho@hotmail.com"
    },
    "journey": {
        "title": "Trajetória do Trader",
        "description": "Progressão de aprendizado do iniciante ao trader profissional",
        "stages": [
            {"level": 1, "name": "Conhecimentos Básicos", "progress": 17},
            {"level": 2, "name": "Conhecendo o Método", "progress": 33},
            {"level": 3, "name": "Reconhecendo os Setups", "progress": 50},
            {"level": 4, "name": "Refino dos Setups", "progress": 67},
            {"level": 5, "name": "Consistência no Simulador", "progress": 83},
            {"level": 6, "name": "Conta Real com 2 Contratos", "progress": 100}
        ]
    },
    "modules": []
}

# Processar cada módulo
for mod_idx, (mod_name, mod_info) in enumerate(modules_sorted, 1):
    pages = mod_info['pages']
    topics_list = mod_info['topics']

    module = {
        "id": f"module-{mod_idx:02d}",
        "order": mod_idx,
        "title": mod_name,
        "pages_total": len(pages),
        "images_total": sum(len(pdf_data['pages'][p-1].get('images', [])) for p in pages),
        "topics": []
    }

    # Distribuir páginas entre tópicos
    pages_sorted = sorted(pages)
    pages_per_topic = max(1, len(pages_sorted) // len(topics_list))

    for topic_idx, topic_name in enumerate(topics_list, 1):
        topic = {
            "id": f"module-{mod_idx:02d}-topic-{topic_idx:02d}",
            "order": topic_idx,
            "title": topic_name,
            "slides": []
        }

        # Determinar páginas para este tópico
        start_idx = (topic_idx - 1) * pages_per_topic
        if topic_idx == len(topics_list):
            end_idx = len(pages_sorted)  # Último tópico pega resto das páginas
        else:
            end_idx = topic_idx * pages_per_topic

        topic_pages = pages_sorted[start_idx:end_idx]

        # Criar slides a partir das páginas
        for slide_idx, page_num in enumerate(topic_pages, 1):
            page_pdf = pdf_data['pages'][page_num - 1]
            page_text = pages_dict.get(page_num, "")

            slide = {
                "id": f"module-{mod_idx:02d}-slide-{slide_idx:03d}",
                "page_number": page_num,
                "title": topic_name,
                "content_preview": page_text[:300] if page_text else "",
                "content_full": page_text,
                "layout_type": "standard",
                "images": [],
                "tables": [],
                "metadata": {
                    "reading_time_minutes": max(1, len(page_text) // 250),
                    "content_length": len(page_text),
                    "has_images": len(page_pdf.get('images', [])) > 0,
                    "has_tables": len(page_pdf.get('tables', [])) > 0
                },
                "seo": {
                    "title": f"{topic_name} - Método Price Action Oliver Velez",
                    "description": f"Aprenda {topic_name.lower()} no curso de trading Price Action da FIMATHE",
                    "keywords": f"trading, price action, {topic_name.lower()}, Oliver Velez, FIMATHE"
                }
            }

            # Processar imagens da página
            for img_idx, img in enumerate(page_pdf.get('images', []), 1):
                image = {
                    "id": f"img-{page_num:03d}-{img_idx:02d}",
                    "src": f"apostila-module-{mod_idx}-page-{page_num:03d}-{img_idx:02d}.webp",
                    "src_fallback": f"apostila-module-{mod_idx}-page-{page_num:03d}-{img_idx:02d}.png",
                    "alt": f"{topic_name} - Ilustração {img_idx} (página {page_num})",
                    "caption": f"Fig. {page_num}.{img_idx}",
                    "type": "chart" if img.get('width', 0) > 300 else "icon",
                    "dimensions": {
                        "width": int(img.get('width', 0)),
                        "height": int(img.get('height', 0))
                    },
                    "position": {
                        "x": int(img.get('x0', 0)),
                        "y": int(img.get('top', 0))
                    },
                    "priority": "high" if img.get('width', 0) > 400 else "normal",
                    "page_source": page_num,
                    "optimization": {
                        "webp_enabled": True,
                        "lazy_load": True,
                        "srcset": True
                    }
                }
                slide['images'].append(image)

            # Processar tabelas da página
            for tbl_idx, table in enumerate(page_pdf.get('tables', []), 1):
                table_obj = {
                    "id": f"table-{page_num:03d}-{tbl_idx:02d}",
                    "caption": f"Tabela {page_num}.{tbl_idx}",
                    "data": table,
                    "page_source": page_num,
                    "responsive": True
                }
                slide['tables'].append(table_obj)

            topic['slides'].append(slide)

        module['topics'].append(topic)

    landing_page_data['modules'].append(module)

print(f"  ✓ {len(landing_page_data['modules'])} módulos estruturados")
print(f"  ✓ {landing_page_data['metadata']['total_topics']} tópicos extraídos")
print(f"  ✓ {landing_page_data['metadata']['total_slides']} slides criados")

# ============================================================================
# FASE 5: SALVAR E VALIDAR
# ============================================================================

print("\n[FASE 5/5] Salvando e validando...")

output_path = Path('landing-page-data.json')

try:
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(landing_page_data, f, ensure_ascii=False, indent=2)

    file_size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"  ✓ Arquivo salvo: {output_path}")
    print(f"  ✓ Tamanho: {file_size_mb:.2f} MB")

    # Validação
    validation = {
        "modules": len(landing_page_data['modules']) == landing_page_data['metadata']['total_modules'],
        "slides": sum(len(t['slides']) for m in landing_page_data['modules'] for t in m['topics']) == landing_page_data['metadata']['total_slides'],
        "all_images_have_alt": all(
            img.get('alt') for m in landing_page_data['modules']
            for t in m['topics'] for s in t['slides'] for img in s['images']
        ),
        "all_slides_have_seo": all(
            s.get('seo') for m in landing_page_data['modules']
            for t in m['topics'] for s in t['slides']
        )
    }

    print("\n  Validações:")
    for check, result in validation.items():
        status = "✓" if result else "✗"
        print(f"    {status} {check}: {result}")

    print("\n" + "=" * 80)
    print("✓ PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
    print("=" * 80)
    print(f"\nArquivo JSON consolidado pronto para landing page:")
    print(f"  📄 {output_path}")
    print(f"  📊 {landing_page_data['metadata']['total_modules']} módulos")
    print(f"  📑 {landing_page_data['metadata']['total_slides']} slides")
    print(f"  🖼️  {landing_page_data['metadata']['total_images']} imagens")
    print(f"  📋 {landing_page_data['metadata']['total_tables']} tabelas")
    print()

except Exception as e:
    print(f"  ✗ Erro ao salvar arquivo: {e}")
    exit(1)
