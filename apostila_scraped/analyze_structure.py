#!/usr/bin/env python3
"""
Analisador de Estrutura - Identifica módulos, tópicos e limite de páginas
Saída: Relatório em texto com estrutura detalhada para uso no gerador JSON
"""

import json
import re
from collections import defaultdict

# Carregar dados
with open('pdf_extracted.json', 'r', encoding='utf-8') as f:
    pdf_data = json.load(f)

with open('pdf_texto_completo.txt', 'r', encoding='utf-8') as f:
    pdf_text = f.read()

# ============================================================================
# 1. PARSING DE ESTRUTURA
# ============================================================================

print("=" * 80)
print("ANÁLISE DE ESTRUTURA - Apostila FIMATHE Price Action")
print("=" * 80)

# Extrair módulos
modules_found = re.findall(r'^Módulo\s+(.+?)$', pdf_text, re.MULTILINE)
pages_found = re.findall(r'^PAGINA\s+(\d+)$', pdf_text, re.MULTILINE)

print(f"\n✓ {len(pdf_data['pages'])} páginas no PDF")
print(f"✓ {len(pages_found)} marcadores de página no texto")
print(f"✓ {len(modules_found)} módulos encontrados:\n")

for i, mod in enumerate(modules_found, 1):
    print(f"  {i}. {mod}")

# ============================================================================
# 2. MAPEAR PÁGINA → MÓDULO
# ============================================================================

print("\n" + "=" * 80)
print("MAPEAMENTO: PÁGINA → MÓDULO")
print("=" * 80)

page_to_module = {}
current_module = None
current_module_start = None

for page_num in range(1, len(pdf_data['pages']) + 1):
    page_text = pdf_data['pages'][page_num - 1].get('text', '')

    # Procurar por "Módulo X" no texto da página
    if 'Módulo' in page_text:
        match = re.search(r'Módulo\s+(.+?)(?:\n|$)', page_text)
        if match:
            current_module = match.group(1)
            current_module_start = page_num
            page_to_module[page_num] = current_module
    elif current_module:
        page_to_module[page_num] = current_module

# Agrupar páginas por módulo
modules_pages = defaultdict(list)
for page_num, mod_name in page_to_module.items():
    modules_pages[mod_name].append(page_num)

print("\nMódulos e suas páginas:\n")
for mod_idx, (mod_name, pages) in enumerate(sorted(modules_pages.items(), key=lambda x: min(x[1])), 1):
    page_range = f"{min(pages)}-{max(pages)}"
    total_pages = len(pages)
    images_count = sum(len(pdf_data['pages'][p-1].get('images', [])) for p in pages)
    tables_count = sum(len(pdf_data['pages'][p-1].get('tables', [])) for p in pages)

    print(f"\n{mod_idx}. {mod_name}")
    print(f"   Páginas: {page_range} (total: {total_pages})")
    print(f"   Imagens: {images_count} | Tabelas: {tables_count}")

# ============================================================================
# 3. ESTATÍSTICAS FINAIS
# ============================================================================

print("\n" + "=" * 80)
print("ESTATÍSTICAS CONSOLIDADAS")
print("=" * 80)

total_images = sum(len(page.get('images', [])) for page in pdf_data['pages'])
total_tables = sum(len(page.get('tables', [])) for page in pdf_data['pages'])
total_text = sum(len(page.get('text', '')) for page in pdf_data['pages'])

print(f"\nTotal Geral:")
print(f"  ✓ Páginas: {len(pdf_data['pages'])}")
print(f"  ✓ Módulos: {len(modules_pages)}")
print(f"  ✓ Imagens: {total_images}")
print(f"  ✓ Tabelas: {total_tables}")
print(f"  ✓ Caracteres de texto: {total_text:,}")
print(f"  ✓ Média de imagens por página: {total_images / len(pdf_data['pages']):.1f}")
print(f"  ✓ Média de caracteres por página: {total_text / len(pdf_data['pages']):.0f}")

# ============================================================================
# 4. TÓPICOS ENCONTRADOS
# ============================================================================

print("\n" + "=" * 80)
print("TÓPICOS ENCONTRADOS (no primeiro parágrafo após cada módulo)")
print("=" * 80)

for mod_idx, (mod_name, pages) in enumerate(sorted(modules_pages.items(), key=lambda x: min(x[1])), 1):
    start_page = min(pages) + 1  # Próxima página após início do módulo
    if start_page <= len(pdf_data['pages']):
        page_text = pdf_data['pages'][start_page - 1].get('text', '')
        # Extrair primeiras linhas como tópicos
        lines = [l.strip() for l in page_text.split('\n') if l.strip()]
        topics = [l for l in lines[:10] if len(l) < 100]  # Linhas curtas = tópicos

        print(f"\n{mod_idx}. {mod_name}")
        for topic in topics[:5]:
            print(f"   • {topic}")

print("\n" + "=" * 80)
print("✓ Análise completa!")
print("=" * 80)
