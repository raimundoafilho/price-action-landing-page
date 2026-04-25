# -*- coding: utf-8 -*-
import os
import sys
import fitz  # PyMuPDF

# Configurar encoding para Windows
sys.stdout.reconfigure(encoding='utf-8')

# Caminho do PDF
pdf_path = r'C:\PROJETO-IA\TRADE\Oliver-Velez-Metodo\Apostila Ariane Campolim_2324 (1).pdf'
output_dir = r'C:\PROJETO-IA\TRADE\apostila_scraped\images'

# Criar diretório se não existir
os.makedirs(output_dir, exist_ok=True)

print("[*] Abrindo PDF com PyMuPDF...")
try:
    # Abrir PDF
    pdf_document = fitz.open(pdf_path)
    total_pages = len(pdf_document)

    print(f"[INFO] Total de páginas: {total_pages}")
    print("[*] Convertendo páginas em imagens (DPI 150)...")

    for page_num in range(total_pages):
        page = pdf_document[page_num]

        # Renderizar página como pixmap (DPI 150 = zoom 1.25)
        # DPI 72 é padrão, então 150 DPI = 150/72 = 2.08 de zoom
        zoom = 150 / 72
        matrix = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=matrix, alpha=False)

        # Salvar como PNG
        page_num_display = page_num + 1
        filename = f"{output_dir}/page_{page_num_display:03d}.png"
        pix.save(filename)

        if page_num_display % 50 == 0:
            print(f"[OK] {page_num_display} páginas convertidas...")

    pdf_document.close()

    print(f"[SUCESSO] Total: {total_pages} páginas convertidas em imagens!")
    print(f"[PASTA] Salvas em: {output_dir}/")

except Exception as e:
    print(f"[ERRO] {e}")
    import traceback
    traceback.print_exc()
