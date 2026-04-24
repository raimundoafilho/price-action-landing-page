#!/usr/bin/env python3
"""
Extrator de imagens do PDF para pipeline de landing page.
Extrai 877 imagens usando coordenadas do pdf_extracted.json.
"""

import json
import pdfplumber
from pathlib import Path
from PIL import Image
import io
import sys

def extract_images_from_pdf():
    """Extrai imagens do PDF usando coordenadas do JSON extraído."""

    # Caminhos
    pdf_path = Path("Oliver-Velez-Metodo/Apostila Ariane Campolim_2324 (1).pdf")
    json_path = Path("apostila_scraped/pdf_extracted.json")
    output_dir = Path("apostila_scraped/images-original")

    # Criar pasta
    output_dir.mkdir(parents=True, exist_ok=True)

    # Carregar metadata das imagens
    with open(json_path, 'r', encoding='utf-8') as f:
        extracted = json.load(f)

    print(f"📄 Abrindo PDF: {pdf_path}")
    print(f"📋 Usando metadata de: {json_path}")
    print(f"💾 Salvando em: {output_dir}")
    print()

    total_extracted = 0
    failed_count = 0
    errors = []

    with pdfplumber.open(pdf_path) as pdf:
        print(f"Total de páginas no PDF: {len(pdf.pages)}")
        print(f"Total de imagens a extrair: {sum(len(p.get('images', [])) for p in extracted['pages'])}")
        print()

        for page_data in extracted['pages']:
            page_num = page_data['page_number']
            images = page_data.get('images', [])

            if not images:
                continue

            if page_num > len(pdf.pages):
                print(f"⚠️  Página {page_num} fora do intervalo (PDF tem {len(pdf.pages)} páginas)")
                continue

            pdf_page = pdf.pages[page_num - 1]  # Zero-indexed

            for img_idx, img_coords in enumerate(images, 1):
                try:
                    # Extrair usando coordenadas
                    x0 = img_coords['x0']
                    top = img_coords['top']
                    width = img_coords['width']
                    height = img_coords['height']

                    # Garantir valores válidos
                    if width <= 0 or height <= 0:
                        errors.append(f"Página {page_num}, imagem {img_idx}: dimensões inválidas ({width}x{height})")
                        failed_count += 1
                        continue

                    # Calcular retângulo (pode haver offsets negativos)
                    x1 = x0 + width
                    bottom = top + height

                    # Clipping para estar dentro da página
                    crop_box = (
                        max(0, x0),
                        max(0, top),
                        min(pdf_page.width, x1),
                        min(pdf_page.height, bottom)
                    )

                    # Extrair imagem usando PIL
                    try:
                        im = pdf_page.within_bbox(crop_box).crop(crop_box)
                        if im.size[0] <= 0 or im.size[1] <= 0:
                            errors.append(f"Página {page_num}, imagem {img_idx}: imagem vazia após crop")
                            failed_count += 1
                            continue
                    except Exception as e:
                        # Tentar com pdfminer como fallback
                        try:
                            im = pdf_page.crop(crop_box).to_image()
                            if not im or im.size[0] <= 0:
                                raise ValueError("Imagem vazia")
                        except:
                            errors.append(f"Página {page_num}, imagem {img_idx}: falha na extração - {str(e)}")
                            failed_count += 1
                            continue

                    # Salvar com nome estruturado
                    filename = f"page-{page_num:03d}-image-{img_idx:02d}.original"
                    filepath = output_dir / filename

                    # Converter para PNG temporário
                    if im.mode == 'RGBA':
                        # Converter para RGB com fundo branco para JPEG
                        rgb_im = Image.new('RGB', im.size, (255, 255, 255))
                        rgb_im.paste(im, mask=im.split()[3] if len(im.split()) == 4 else None)
                        rgb_im.save(filepath.with_suffix('.jpg'), quality=95)
                    else:
                        im.convert('RGB').save(filepath.with_suffix('.jpg'), quality=95)

                    total_extracted += 1

                    if total_extracted % 100 == 0:
                        print(f"✓ Extraídas {total_extracted} imagens...")

                except Exception as e:
                    errors.append(f"Página {page_num}, imagem {img_idx}: {str(e)}")
                    failed_count += 1
                    continue

    # Relatório
    print()
    print("=" * 60)
    print("📊 RELATÓRIO DE EXTRAÇÃO")
    print("=" * 60)
    print(f"✅ Imagens extraídas com sucesso: {total_extracted}")
    print(f"❌ Falhas: {failed_count}")
    print(f"📁 Salvas em: {output_dir}")
    print(f"💾 Total de arquivos: {len(list(output_dir.glob('*.jpg')))}")

    if errors:
        print("\n⚠️  Erros encontrados:")
        for error in errors[:10]:  # Mostrar primeiros 10
            print(f"  - {error}")
        if len(errors) > 10:
            print(f"  ... e mais {len(errors)-10} erros")

    return total_extracted, failed_count

if __name__ == "__main__":
    extract_images_from_pdf()
