# -*- coding: utf-8 -*-
import os
import sys
import json
import fitz

# Configurar encoding para Windows
sys.stdout.reconfigure(encoding='utf-8')

# Caminhos
pdf_path = r'C:\PROJETO-IA\TRADE\Oliver-Velez-Metodo\Apostila Ariane Campolim_2324 (1).pdf'
output_file = r'C:\PROJETO-IA\TRADE\apostila_scraped\image_mapping.json'
images_dir = r'C:\PROJETO-IA\TRADE\apostila_scraped\images'

print("[*] Criando arquivo de mapeamento semântico...")

try:
    # Abrir PDF para extrair metadados e TOC
    pdf = fitz.open(pdf_path)
    total_pages = len(pdf)

    # Inicializar estrutura de mapeamento
    mapping = {
        "metadata": {
            "total_pages": total_pages,
            "extraction_date": "2026-04-24",
            "method": "PyMuPDF (fitz) - DPI 150",
            "dpi": 150,
            "source_pdf": "Apostila Ariane Campolim_2324 (1).pdf",
            "content_type": "Trading - Price Action Education (Oliver Velez / iFund Traders)"
        },
        "pages": {}
    }

    # Tentar extrair TOC (Table of Contents)
    toc = pdf.get_toc()
    print(f"[INFO] Índice com {len(toc)} entradas encontrado" if toc else "[INFO] Nenhum índice estruturado no PDF")

    # Criar mapeamento para cada página
    for page_num in range(total_pages):
        page_num_display = page_num + 1

        # Buscar seção correspondente no TOC
        section = "Conteúdo"
        subsection = "Sem classificação"

        # Procurar pelo índice
        if toc:
            for toc_level, toc_title, toc_page in toc:
                if toc_page <= page_num_display:
                    if toc_level == 1:
                        section = toc_title
                    elif toc_level == 2:
                        subsection = toc_title

        # Extrair texto da página para descrição
        page = pdf[page_num]
        text = page.get_text()[:200]  # Primeiros 200 caracteres
        description = text.replace('\n', ' ').strip() if text else f"Página {page_num_display}"

        # Entrada de mapeamento
        mapping["pages"][str(page_num_display)] = {
            "page_number": page_num_display,
            "image_file": f"page_{page_num_display:03d}.png",
            "section": section,
            "subsection": subsection,
            "description": description,
            "width": int(page.rect.width),
            "height": int(page.rect.height)
        }

        if page_num_display % 50 == 0:
            print(f"[OK] Mapeadas {page_num_display}/{total_pages} páginas...")

    pdf.close()

    # Salvar arquivo JSON
    output_dir = os.path.dirname(output_file)
    os.makedirs(output_dir, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)

    print(f"[SUCESSO] Mapeamento criado com {total_pages} páginas")
    print(f"[ARQUIVO] Salvo em: {output_file}")
    print(f"[TAMANHO] {os.path.getsize(output_file) / 1024:.1f} KB")

except Exception as e:
    print(f"[ERRO] {e}")
    import traceback
    traceback.print_exc()
