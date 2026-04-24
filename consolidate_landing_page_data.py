#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Consolidador de dados para landing page - Apostila de Trading
Consolida:
1. PDF extraído (páginas, texto, imagens)
2. Análise de imagens (estatísticas, tipos)
3. Estrutura de módulos e tópicos
4. Definições de layout
Gera: landing-page-data.json (~2MB)
"""

import json
import re
import sys
import io
from pathlib import Path
from typing import Any, Dict, List, Optional
from collections import defaultdict
import hashlib

# Força UTF-8 no stdout para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Configurações
PDF_EXTRACTED = r"C:\PROJETO-IA\TRADE\apostila_scraped\pdf_extracted.json"
PDF_TEXTO = r"C:\PROJETO-IA\TRADE\apostila_scraped\pdf_texto_completo.txt"
IMAGE_ANALYSIS = r"C:\PROJETO-IA\TRADE\apostila_scraped\image_analysis.json"
OUTPUT_FILE = r"C:\PROJETO-IA\TRADE\apostila_scraped\landing-page-data.json"

# Definições de modules (estrutura descoberta no PDF)
MODULES_STRUCTURE = [
    {
        "id": "mod-basic-1",
        "order": 1,
        "title": "Módulo Básico 1 - Conhecimentos Básicos",
        "topics": ["bolsa-valores", "tipos-traders", "corretora"]
    },
    {
        "id": "mod-basic-2",
        "order": 2,
        "title": "Módulo Básico 2 - Introdução ao Método",
        "topics": ["candles", "controle-forcas", "barra-elefante", "indicadores", "setups-tendencia"]
    },
    {
        "id": "mod-intermediate-1",
        "order": 3,
        "title": "Módulo Intermediário 1",
        "topics": []
    },
    {
        "id": "mod-intermediate-2",
        "order": 4,
        "title": "Módulo Intermediário 2",
        "topics": []
    },
    {
        "id": "mod-advanced",
        "order": 5,
        "title": "Módulo Avançado",
        "topics": []
    },
]

# Mapa de layout tipos
LAYOUT_TYPES = {
    "stack": "Imagens empilhadas verticalmente",
    "2col": "Duas colunas - imagem e texto lado a lado",
    "fluida": "Layout responsivo fluido",
    "grid": "Grid de múltiplos itens"
}

# Mapa de tipos de imagem
IMAGE_TYPES = {
    "chart": "Gráfico/análise técnica",
    "screenshot": "Captura de tela",
    "table": "Tabela/dados",
    "diagram": "Diagrama/fluxo",
    "annotation": "Anotação/exemplos",
    "icon": "Ícone/símbolo",
    "logo": "Logo/branding",
    "unknown": "Desconhecido"
}


class LandingPageDataConsolidator:
    """Consolida dados de múltiplas fontes em um JSON único hierárquico."""

    def __init__(self):
        self.pdf_data = None
        self.image_analysis = None
        self.pdf_text = None
        self.topics_by_page = defaultdict(list)
        self.images_by_page = defaultdict(list)
        self.page_content_map = {}

    def load_sources(self):
        """Carrega todos os arquivos de fonte."""
        print("Carregando fontes de dados...")

        # PDF extraído
        with open(PDF_EXTRACTED, 'r', encoding='utf-8') as f:
            self.pdf_data = json.load(f)
        print(f"  [OK] PDF extraido: {len(self.pdf_data['pages'])} paginas")

        # Análise de imagens
        with open(IMAGE_ANALYSIS, 'r', encoding='utf-8') as f:
            self.image_analysis = json.load(f)
        print(f"  [OK] Analise de imagens: {self.image_analysis['summary']['totalImages']} imagens")

        # PDF texto
        with open(PDF_TEXTO, 'r', encoding='utf-8') as f:
            self.pdf_text = f.read()
        print(f"  [OK] PDF texto completo: {len(self.pdf_text)} caracteres")

    def parse_pdf_text_structure(self) -> Dict[int, str]:
        """Extrai estrutura de topicos do texto do PDF."""
        print("\nParsando estrutura de topicos...")

        topics_map = {}
        lines = self.pdf_text.split('\n')

        for i, line in enumerate(lines):
            # Identifica títulos de tópicos
            if any(keyword in line for keyword in
                   ['CONHECIMENTOS', 'INTRODUÇÃO', 'Análise', 'Controle',
                    'Barra', 'Tempos', 'Indicadores', 'Tipos', 'Bolsa']):
                topics_map[i] = line.strip()

        print(f"  ✓ {len(topics_map)} tópicos identificados")
        return topics_map

    def classify_image_type(self, page_num: int, image_index: int,
                           dimensions: Dict) -> str:
        """Classifica tipo de imagem baseado em heurística."""
        width = dimensions.get('width', 0)
        height = dimensions.get('height', 0)
        aspect_ratio = width / height if height > 0 else 1

        # Heurísticas de classificação
        if width > 400 and height > 200:  # Grande, provavelmente gráfico
            return "chart"
        elif width < 150 and height < 150:  # Pequeno, provavelmente ícone
            return "icon"
        elif 0.5 < aspect_ratio < 2:  # Quadrado/quase, tabela ou anotação
            return "annotation"
        elif aspect_ratio > 2:  # Muito largo
            return "screenshot"
        else:
            return "unknown"

    def get_responsive_dimensions(self, original_width: float) -> Dict[str, Dict]:
        """Calcula dimensões responsivas otimizadas por breakpoint."""
        return {
            "desktop": {
                "width": min(int(original_width * 0.8), 580),
                "height": "auto"
            },
            "tablet": {
                "width": min(int(original_width * 0.6), 460),
                "height": "auto"
            },
            "mobile": {
                "width": "100%",
                "maxWidth": "calc(100% - 40px)",
                "height": "auto"
            }
        }

    def build_modules_with_slides(self) -> List[Dict]:
        """Constrói estrutura hierárquica de módulos → tópicos → slides."""
        print("\nConstituindo estrutura hierárquica...")

        modules = []
        slide_counter = 1

        for page in self.pdf_data['pages']:
            page_num = page['page_number']
            text = page.get('text', '')
            images = page.get('images', [])
            tables = page.get('tables', [])

            # Determinar módulo e tópico
            module_id = self._determine_module(text)
            topic_id = self._determine_topic(text)

            # Processar imagens da página
            page_images = []
            for img_idx, img in enumerate(images):
                image_type = self.classify_image_type(page_num, img_idx, img)
                priority = "high" if img_idx < 2 else "medium" if img_idx < 4 else "low"

                # Gerar nome WebP
                webp_name = f"slide-{slide_counter:03d}-img-{img_idx+1:02d}.webp"

                page_images.append({
                    "id": f"img-{page_num}-{img_idx+1}",
                    "src": webp_name,
                    "alt": f"Imagem {img_idx+1} do slide {slide_counter}",
                    "caption": f"Conteúdo visual - Slide {slide_counter}",
                    "type": image_type,
                    "width": int(img.get('width', 0)),
                    "height": int(img.get('height', 0)),
                    "responsive": self.get_responsive_dimensions(img.get('width', 400)),
                    "priority": priority
                })

            # Determinar layout baseado em número e tipo de imagens
            layout_type = self._assign_layout_type(len(page_images), len(tables), text)

            # Extrair conteúdo principal
            slide_content = self._extract_slide_content(text)

            # Criar slide
            slide = {
                "id": f"slide-{slide_counter:03d}",
                "slide_number": slide_counter,
                "page_number": page_num,
                "title": self._extract_title(text),
                "content": slide_content,
                "layout_type": layout_type,
                "images": page_images,
                "tables": [self._format_table(t) for t in tables] if tables else [],
                "seo_metadata": {
                    "title": self._extract_title(text),
                    "description": slide_content[:160] if slide_content else "",
                    "keywords": [module_id, topic_id, "trading", "price-action"]
                }
            }

            self.topics_by_page[page_num] = {
                "module_id": module_id,
                "topic_id": topic_id,
                "slide": slide
            }

            slide_counter += 1

        # Agrupar slides em módulos
        modules = self._group_slides_into_modules()

        print(f"  ✓ {len(modules)} módulos com {slide_counter-1} slides total")
        return modules

    def _determine_module(self, text: str) -> str:
        """Determina ID do módulo baseado no texto."""
        if "Módulo Básico 1" in text or "CONHECIMENTOS BÁSICOS" in text:
            return "mod-basic-1"
        elif "Módulo Básico 2" in text or "INTRODUÇÃO AO MÉTODO" in text:
            return "mod-basic-2"
        elif "Módulo Intermediário 1" in text:
            return "mod-intermediate-1"
        elif "Módulo Intermediário 2" in text:
            return "mod-intermediate-2"
        elif "Módulo Avançado" in text:
            return "mod-advanced"
        return "mod-unknown"

    def _determine_topic(self, text: str) -> str:
        """Determina ID do tópico baseado no texto."""
        text_lower = text.lower()

        topic_map = {
            "bolsa": "bolsa-valores",
            "trader": "tipos-traders",
            "corretora": "corretora",
            "candle": "candles",
            "controle": "controle-forcas",
            "barra": "barra-elefante",
            "indicador": "indicadores",
            "setup": "setups",
            "análise": "analise-grafica"
        }

        for keyword, topic_id in topic_map.items():
            if keyword in text_lower:
                return topic_id

        return "tópico-geral"

    def _assign_layout_type(self, num_images: int, num_tables: int,
                           text: str) -> str:
        """Atribui tipo de layout baseado em conteúdo."""
        if num_images > 3:
            return "stack" if num_images > 5 else "2col"
        elif num_tables > 0:
            return "2col"
        elif "passo" in text.lower() or "exemplo" in text.lower():
            return "grid"
        else:
            return "stack"

    def _extract_title(self, text: str) -> str:
        """Extrai título do texto da página."""
        lines = text.split('\n')
        for line in lines[:5]:
            if line.strip() and len(line.strip()) < 100:
                return line.strip()
        return "Sem título"

    def _extract_slide_content(self, text: str) -> str:
        """Extrai conteúdo principal do slide."""
        # Remove página número e rodapé
        text = re.sub(r'Licenciado para.*', '', text)
        text = re.sub(r'\d+\s*$', '', text, flags=re.MULTILINE)
        return text.strip()[:500]

    def _format_table(self, table: List[List[Any]]) -> Dict:
        """Formata tabela extraída."""
        if not table:
            return {}

        return {
            "rows": len(table),
            "cols": len(table[0]) if table else 0,
            "data": table
        }

    def _group_slides_into_modules(self) -> List[Dict]:
        """Agrupa slides em módulos com tópicos."""
        modules_dict = {m['id']: m for m in MODULES_STRUCTURE}

        # Agrupar slides por módulo
        slides_by_module = defaultdict(list)
        for page_num, data in self.topics_by_page.items():
            module_id = data['module_id']
            slides_by_module[module_id].append(data['slide'])

        # Construir estrutura final
        result = []
        for module in MODULES_STRUCTURE:
            module_id = module['id']
            slides = sorted(slides_by_module[module_id],
                          key=lambda s: s['slide_number'])

            result.append({
                "id": module_id,
                "order": module['order'],
                "title": module['title'],
                "slides_total": len(slides),
                "topics": [
                    {
                        "id": topic_id,
                        "title": self._format_topic_title(topic_id),
                        "slides": [s for s in slides
                                 if s['seo_metadata']['keywords'][1] == topic_id]
                    }
                    for topic_id in module['topics']
                ],
                "all_slides": slides
            })

        return result

    def _format_topic_title(self, topic_id: str) -> str:
        """Formata título do tópico a partir do ID."""
        return topic_id.replace('-', ' ').title()

    def build_output(self, modules: List[Dict]) -> Dict:
        """Constrói objeto de saída final."""
        print("\nConstituindo arquivo de saída final...")

        return {
            "metadata": {
                "title": "Apostila de Trading - Price Action",
                "description": "Apostila completa de Price Action com estrutura hierárquica de módulos, tópicos e slides",
                "generated_at": self._get_timestamp(),
                "total_modules": len(modules),
                "total_slides": sum(m['slides_total'] for m in modules),
                "total_images": self.image_analysis['summary']['totalImages'],
                "pages": len(self.pdf_data['pages']),
                "author": "Ariane Campolim",
                "subject": "Trading, Price Action, Análise Técnica"
            },
            "config": {
                "layout_types": LAYOUT_TYPES,
                "image_types": IMAGE_TYPES,
                "responsive_breakpoints": {
                    "mobile": 480,
                    "tablet": 768,
                    "desktop": 1024,
                    "large": 1440
                }
            },
            "image_analysis": self.image_analysis,
            "modules": modules
        }

    def _get_timestamp(self) -> str:
        """Retorna timestamp ISO."""
        from datetime import datetime
        return datetime.now().isoformat()

    def save_output(self, data: Dict):
        """Salva arquivo JSON final."""
        print(f"\nSalvando em {OUTPUT_FILE}...")

        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        # Calcular tamanho
        file_size = Path(OUTPUT_FILE).stat().st_size / (1024 * 1024)
        print(f"  ✓ Arquivo salvo: {file_size:.2f}MB")

    def run(self):
        """Executa consolidação completa."""
        print("=" * 70)
        print("CONSOLIDADOR DE DADOS - LANDING PAGE")
        print("=" * 70)

        self.load_sources()
        modules = self.build_modules_with_slides()
        output = self.build_output(modules)
        self.save_output(output)

        print("\n" + "=" * 70)
        print("CONSOLIDAÇÃO CONCLUÍDA COM SUCESSO")
        print("=" * 70)
        print(f"\nResumo:")
        print(f"  • Módulos: {output['metadata']['total_modules']}")
        print(f"  • Slides: {output['metadata']['total_slides']}")
        print(f"  • Imagens: {output['metadata']['total_images']}")
        print(f"  • Páginas PDF: {output['metadata']['pages']}")
        print(f"  • Arquivo: {OUTPUT_FILE}")


if __name__ == "__main__":
    consolidator = LandingPageDataConsolidator()
    consolidator.run()
