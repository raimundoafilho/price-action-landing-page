#!/usr/bin/env python3
"""
Gerador de Landing Page JSON - Apostila FIMATHE Price Action
Estrutura: 7 módulos → tópicos → slides → conteúdo + imagens + tabelas
"""

import json
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# ============================================================================
# 1. CONFIGURAÇÃO
# ============================================================================

MODULES_STRUCTURE = {
    "mod-basic-1": {
        "order": 1,
        "title": "Módulo Básico 1 - Conhecimentos Básicos",
        "subtitle": "Fundamentos para começar a operar",
        "topics": [
            "Bolsa de Valores",
            "Tipos de Traders",
            "Corretora"
        ],
        "page_start": 3,
        "page_end": 7
    },
    "mod-basic-2": {
        "order": 2,
        "title": "Módulo Básico 2 - Introdução ao Método",
        "subtitle": "Começando a entender o método Price Action",
        "topics": [
            "Análise dos Candles",
            "Controle de Forças",
            "Barra Elefante, Lei da Continuidade e Regra dos 2/3",
            "Tempos Gráficos Analíticos",
            "Indicadores: Médias Móveis, MACD e Volume",
            "Lei de 3, 5 e 8 Barras",
            "Setups à Favor da Tendência",
            "Setups Contra à Tendência"
        ],
        "page_start": 8,
        "page_end": 60
    },
    "mod-intermediate-1": {
        "order": 3,
        "title": "Módulo Intermediário 1 - Reconhecendo os Setups",
        "subtitle": "Identificação prática dos padrões",
        "topics": [
            "Setup 1 - Push",
            "Setup 2 - Pull Back",
            "Setup 3 - Acumulação",
            "Filtragem por Tendência",
            "Filtragem por Volatilidade"
        ],
        "page_start": 61,
        "page_end": 100
    },
    "mod-intermediate-2": {
        "order": 4,
        "title": "Módulo Intermediário 2 - Refino dos Setups",
        "subtitle": "Técnicas avançadas de entrada e saída",
        "topics": [
            "Afunilamento de Preço",
            "Dinâmica de Mercado",
            "Confirmação de Setups",
            "Gestão de Risco"
        ],
        "page_start": 101,
        "page_end": 140
    },
    "mod-advanced": {
        "order": 5,
        "title": "Módulo Avançado - Consistência no Simulador e Conta Real",
        "subtitle": "Da prática à execução real",
        "topics": [
            "Operando no Simulador",
            "Transição para Conta Real",
            "Psicologia Operacional",
            "Gerenciamento de Capital",
            "Documentação de Operações",
            "Análise de Desempenho"
        ],
        "page_start": 141,
        "page_end": 180
    }
}

# ============================================================================
# 2. CARREGAR DADOS BRUTOS
# ============================================================================

print("[1/5] Carregando dados extraídos...")

with open('pdf_extracted.json', 'r', encoding='utf-8') as f:
    pdf_data = json.load(f)

with open('pdf_texto_completo.txt', 'r', encoding='utf-8') as f:
    pdf_text = f.read()

# Parsing do texto por página
pages_text = re.split(r'={5,}\nPAGINA\s+(\d+)\n={5,}', pdf_text)
pages_dict = {}

for i in range(1, len(pages_text), 2):
    if i + 1 < len(pages_text):
        page_num = int(pages_text[i])
        page_content = pages_text[i + 1].strip()
        pages_dict[page_num] = page_content

print(f"  ✓ {len(pdf_data['pages'])} páginas no PDF")
print(f"  ✓ {len(pages_dict)} páginas com conteúdo textual")

# ============================================================================
# 3. ESTRUTURA JSON CONSOLIDADA
# ============================================================================

print("[2/5] Estruturando dados por módulo...")

landing_page_data = {
    "metadata": {
        "title": "Método Price Action de Oliver Velez",
        "subtitle": "Mentoria completa com 5 módulos de trading",
        "author": "Oliver Velez",
        "presented_by": "André Trader / FIMATHE",
        "course_type": "Mentoria - Trading",
        "difficulty": ["Básico", "Intermediário", "Avançado"],
        "version": "1.0",
        "created": datetime.now().isoformat(),
        "updated": datetime.now().isoformat(),
        "total_modules": 5,
        "total_slides": 0,  # Atualizar após processamento
        "total_images": len([img for page in pdf_data['pages'] for img in page['images']]),
        "total_tables": sum(len(page['tables']) for page in pdf_data['pages']),
        "total_pages": len(pdf_data['pages']),
        "language": "pt-BR",
        "license": "Licenciado para - Raimundo Araujo Filho | raimundoaraujo.filho@hotmail.com"
    },
    "journey": {
        "title": "Trajetória do Trader",
        "stages": [
            {"level": 1, "name": "Conhecimentos Básicos"},
            {"level": 2, "name": "Conhecendo o Método"},
            {"level": 3, "name": "Reconhecendo os Setups"},
            {"level": 4, "name": "Refino dos Setups"},
            {"level": 5, "name": "Consistência no Simulador"},
            {"level": 6, "name": "Conta Real com 2 Contratos"}
        ]
    },
    "modules": []
}

# ============================================================================
# 4. PROCESSAR MÓDULOS
# ============================================================================

print("[3/5] Processando módulos...")

for mod_key, mod_config in MODULES_STRUCTURE.items():
    module = {
        "id": mod_key,
        "order": mod_config["order"],
        "title": mod_config["title"],
        "subtitle": mod_config.get("subtitle", ""),
        "slides_total": mod_config["page_end"] - mod_config["page_start"] + 1,
        "topics": []
    }

    # Processar tópicos
    slides_allocated = 0
    pages_total = mod_config["page_end"] - mod_config["page_start"] + 1
    slides_per_topic = max(1, pages_total // len(mod_config["topics"]))  # Distribuir páginas

    for topic_idx, topic_name in enumerate(mod_config["topics"], 1):
        topic = {
            "id": f"{mod_key}-topic-{topic_idx}",
            "order": topic_idx,
            "title": topic_name,
            "slides": []
        }

        # Calcular intervalo de páginas para este tópico
        start_idx = mod_config["page_start"] + slides_allocated
        end_idx = min(
            start_idx + slides_per_topic - 1,
            mod_config["page_end"]
        )

        # Ajustar último tópico para usar todas as páginas restantes
        if topic_idx == len(mod_config["topics"]):
            end_idx = mod_config["page_end"]

        # Para cada página no intervalo do tópico
        for page_num in range(start_idx, end_idx + 1):
            if page_num <= len(pdf_data['pages']):
                page_pdf = pdf_data['pages'][page_num - 1]  # 0-indexed
                page_text = pages_dict.get(page_num, "")

                # Criar slide
                slide = {
                    "id": f"slide-{page_num:03d}",
                    "slide_number": page_num,
                    "title": topic_name,
                    "content": page_text[:500] if page_text else "",  # Snippet
                    "content_full": page_text,
                    "layout_type": "standard",
                    "images": [],
                    "tables": [],
                    "seo": {
                        "title": f"{topic_name} - Método Price Action Oliver Velez",
                        "description": f"Aprenda sobre {topic_name.lower()} no curso Price Action FIMATHE FIMATHE",
                        "keywords": f"Price Action, {topic_name.lower()}, trading, Oliver Velez, FIMATHE"
                    },
                    "reading_time_minutes": max(1, len(page_text) // 200),
                    "estimated_content_length": len(page_text)
                }

                # Processar imagens
                for img_idx, img in enumerate(page_pdf.get('images', []), 1):
                    image = {
                        "id": f"img-{page_num:03d}-{img_idx:02d}",
                        "src": f"apostila-module-{mod_config['order']}-page-{page_num:03d}-img-{img_idx:02d}.webp",
                        "src_fallback": f"apostila-module-{mod_config['order']}-page-{page_num:03d}-img-{img_idx:02d}.png",
                        "alt": f"Ilustração: {topic_name} - Página {page_num}, Imagem {img_idx}",
                        "caption": f"Fig. {page_num}.{img_idx}: {topic_name}",
                        "type": "chart" if img.get('width', 0) > 200 else "icon",
                        "width": int(img.get('width', 0)),
                        "height": int(img.get('height', 0)),
                        "position_x": int(img.get('x0', 0)),
                        "position_y": int(img.get('top', 0)),
                        "priority": "high" if img.get('width', 0) > 400 else "normal",
                        "page_source": page_num
                    }
                    slide['images'].append(image)

                # Processar tabelas
                for tbl_idx, table in enumerate(page_pdf.get('tables', []), 1):
                    table_obj = {
                        "id": f"tbl-{page_num:03d}-{tbl_idx:02d}",
                        "caption": f"Tabela {page_num}.{tbl_idx}",
                        "data": table,
                        "page_source": page_num
                    }
                    slide['tables'].append(table_obj)

                topic['slides'].append(slide)

        slides_allocated += (end_idx - start_idx + 1)
        module['topics'].append(topic)

    landing_page_data['modules'].append(module)

# Atualizar metadata
total_slides = sum(
    len(topic['slides'])
    for module in landing_page_data['modules']
    for topic in module['topics']
)
landing_page_data['metadata']['total_slides'] = total_slides
landing_page_data['metadata']['total_modules'] = len(landing_page_data['modules'])

print(f"  ✓ {len(landing_page_data['modules'])} módulos processados")
print(f"  ✓ {total_slides} slides gerados")

# ============================================================================
# 5. SALVAR JSON CONSOLIDADO
# ============================================================================

print("[4/5] Salvando JSON consolidado...")

output_path = Path('landing-page-data.json')
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(landing_page_data, f, ensure_ascii=False, indent=2)

output_size = output_path.stat().st_size / (1024 * 1024)  # MB
print(f"  ✓ Salvo: {output_path}")
print(f"  ✓ Tamanho: {output_size:.2f} MB")

# ============================================================================
# 6. VALIDAÇÃO
# ============================================================================

print("[5/5] Validando estrutura...")

validation_results = {
    "total_modules": len(landing_page_data['modules']),
    "total_topics": sum(len(m['topics']) for m in landing_page_data['modules']),
    "total_slides": total_slides,
    "total_images": sum(len(s['images']) for m in landing_page_data['modules'] for t in m['topics'] for s in t['slides']),
    "total_tables": sum(len(s['tables']) for m in landing_page_data['modules'] for t in m['topics'] for s in t['slides']),
    "all_images_have_alt": all(
        img.get('alt') for m in landing_page_data['modules']
        for t in m['topics'] for s in t['slides'] for img in s['images']
    ),
    "all_images_have_caption": all(
        img.get('caption') for m in landing_page_data['modules']
        for t in m['topics'] for s in t['slides'] for img in s['images']
    ),
    "all_slides_have_content": all(
        s.get('content') for m in landing_page_data['modules']
        for t in m['topics'] for s in t['slides']
    ),
    "all_slides_have_seo": all(
        s.get('seo') for m in landing_page_data['modules']
        for t in m['topics'] for s in t['slides']
    )
}

print("\n" + "="*70)
print("VALIDAÇÃO FINAL")
print("="*70)
for key, value in validation_results.items():
    status = "✓" if value else "✗"
    print(f"{status} {key}: {value}")

print("\n✓ Processamento completo!")
print(f"\nArquivo de saída: {output_path}")
print(f"Tamanho: {output_size:.2f} MB")
print(f"Pronto para renderizar landing page!")
