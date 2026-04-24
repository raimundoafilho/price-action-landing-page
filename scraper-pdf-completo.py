#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PDF Scraper Completo - Extrai texto, imagens e estrutura
Para: Apostila Ariane Campolim (Metodo Oliver Velez)
"""

import pdfplumber
import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Forcar UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def extract_pdf_complete(pdf_path, output_dir='pdf_output'):
    """Extrai TUDO do PDF: texto, tabelas, imagens, estrutura"""

    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    print(f"\n[LOG] Iniciando extracao de: {pdf_path.name}")
    print(f"[LOG] Saida: {output_dir}")
    print("=" * 70)

    data = {
        'file': pdf_path.name,
        'extracted_at': datetime.now().isoformat(),
        'pages': [],
        'stats': {
            'total_pages': 0,
            'total_images': 0,
            'total_tables': 0,
            'total_text_chars': 0
        }
    }

    try:
        with pdfplumber.open(str(pdf_path)) as pdf:
            data['stats']['total_pages'] = len(pdf.pages)
            print(f"[OK] Total de paginas: {len(pdf.pages)}\n")

            for page_num, page in enumerate(pdf.pages, 1):
                print(f"[{page_num:3d}/{len(pdf.pages):3d}] Processando pagina {page_num}...", end=" ", flush=True)

                page_data = {
                    'page_number': page_num,
                    'width': page.width,
                    'height': page.height,
                    'text': page.extract_text() or '',
                    'tables': page.extract_tables() or [],
                    'images': [],
                    'sections': []
                }

                # Contar caracteres
                text_len = len(page_data['text'])
                data['stats']['total_text_chars'] += text_len

                # Extrair imagens
                try:
                    if hasattr(page, 'images') and page.images:
                        for img_idx, img in enumerate(page.images, 1):
                            img_info = {
                                'index': img_idx,
                                'x0': float(img.get('x0', 0)),
                                'top': float(img.get('top', 0)),
                                'width': float(img.get('width', 0)),
                                'height': float(img.get('height', 0))
                            }
                            page_data['images'].append(img_info)
                            data['stats']['total_images'] += 1
                except:
                    pass

                # Contar tabelas
                data['stats']['total_tables'] += len(page_data['tables'])

                # Estruturar secoes (heuristica simples)
                text_lines = page_data['text'].split('\n')
                current_section = None

                for line in text_lines:
                    if line.strip():
                        # Linha em CAPS eh titulo
                        if line.isupper() and len(line.strip()) > 5:
                            if current_section:
                                page_data['sections'].append(current_section)
                            current_section = {
                                'title': line.strip(),
                                'content': []
                            }
                        elif current_section:
                            current_section['content'].append(line.strip())

                if current_section:
                    page_data['sections'].append(current_section)

                data['pages'].append(page_data)

                status = f"[OK] ({text_len} chars, {len(page_data['tables'])} tabelas, {len(page_data['images'])} imgs)"
                print(status)

        print("\n" + "=" * 70)
        print(f"\n[RESUMO] Extracao concluida:")
        print(f"  * Paginas: {data['stats']['total_pages']}")
        print(f"  * Caracteres: {data['stats']['total_text_chars']:,}")
        print(f"  * Tabelas: {data['stats']['total_tables']}")
        print(f"  * Imagens: {data['stats']['total_images']}")

        # Salvar JSON com estrutura completa
        json_path = output_dir / 'pdf_extracted.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n[OK] Dados salvos em: {json_path}")

        # Salvar texto completo
        text_path = output_dir / 'pdf_texto_completo.txt'
        with open(text_path, 'w', encoding='utf-8') as f:
            for page in data['pages']:
                f.write(f"\n{'='*70}\n")
                f.write(f"PAGINA {page['page_number']}\n")
                f.write(f"{'='*70}\n\n")
                f.write(page['text'])
                f.write('\n\n')
        print(f"[OK] Texto salvo em: {text_path}")

        # Salvar resumo
        summary_path = output_dir / 'RESUMO_EXTRACAO.txt'
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(f"RESUMO DE EXTRACAO - {pdf_path.name}\n")
            f.write(f"{'='*70}\n\n")
            f.write(f"Extraido em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
            f.write(f"ESTATISTICAS:\n")
            f.write(f"  * Paginas: {data['stats']['total_pages']}\n")
            f.write(f"  * Caracteres de texto: {data['stats']['total_text_chars']:,}\n")
            f.write(f"  * Tabelas encontradas: {data['stats']['total_tables']}\n")
            f.write(f"  * Imagens encontradas: {data['stats']['total_images']}\n\n")
            f.write(f"ESTRUTURA POR PAGINA:\n\n")

            for page in data['pages']:
                f.write(f"Pagina {page['page_number']}:\n")
                f.write(f"  - Secoes: {len(page['sections'])}\n")
                if page['sections']:
                    for section in page['sections']:
                        title = section['title'][:50] if section['title'] else '(sem titulo)'
                        f.write(f"    * {title}\n")
                f.write(f"  - Tabelas: {len(page['tables'])}\n")
                f.write(f"  - Imagens: {len(page['images'])}\n")
                f.write(f"  - Texto: {len(page['text'])} caracteres\n\n")

        print(f"[OK] Resumo salvo em: {summary_path}")

        print(f"\n[SUCESSO] Extracao concluida com sucesso!")
        return data

    except Exception as e:
        print(f"\n[ERRO] {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Funcao principal"""

    print("\n" + "="*70)
    print("   PDF SCRAPER COMPLETO - Metodo Oliver Velez")
    print("="*70)

    pdf_file = r"C:\PROJETO-IA\TRADE\Oliver-Velez-Metodo\Apostila Ariane Campolim_2324 (1).pdf"

    if not Path(pdf_file).exists():
        print(f"[ERRO] Arquivo nao encontrado: {pdf_file}")
        sys.exit(1)

    # Extrair
    data = extract_pdf_complete(pdf_file, output_dir='apostila_scraped')

    if data:
        print("\n" + "="*70)
        print("[PROXIMO] Proximos passos:")
        print("  1. Revisar dados em: apostila_scraped/pdf_extracted.json")
        print("  2. Criar PRD para landing page")
        print("  3. Gerar landing page HTML profissional")
        print("="*70 + "\n")

if __name__ == '__main__':
    main()
