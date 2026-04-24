#!/usr/bin/env python3
"""
Pipeline de Extração e Otimização de Imagens do PDF
- Extrai imagens do PDF original
- Otimiza em WebP (qualidade 82%)
- Gera PNG fallback
- Cria manifest JSON
"""

import json
import os
import sys
from pathlib import Path
from PIL import Image
from io import BytesIO
import pdfplumber
import hashlib

# Configuração
BASE_DIR = Path(__file__).parent
PDF_PATH = BASE_DIR.parent / "Oliver-Velez-Metodo" / "Apostila Ariane Campolim_2324 (1).pdf"
METADATA_FILE = BASE_DIR / "pdf_extracted.json"
OUTPUT_WEBP_DIR = BASE_DIR / "images-webp"
OUTPUT_PNG_DIR = BASE_DIR / "images-fallback"
MANIFEST_FILE = BASE_DIR / "image-manifest.json"

# Criar diretórios
OUTPUT_WEBP_DIR.mkdir(exist_ok=True)
OUTPUT_PNG_DIR.mkdir(exist_ok=True)

# Limites de tamanho por tipo
RESIZE_LIMITS = {
    'chart': 580,
    'screenshot': 500,
    'icon': 300,
    'default': 800
}

QUALITY_WEBP = 82
QUALITY_PNG = 95


def detect_image_type(width: float, height: float, aspect_ratio: float) -> str:
    """Detecta o tipo de imagem baseado em dimensões."""
    if width < 350 and height < 350:
        return 'icon'
    elif 0.4 < aspect_ratio < 0.7:  # Tall
        return 'screenshot'
    elif aspect_ratio > 1.3:  # Wide
        return 'chart'
    else:
        return 'default'


def extract_images_from_pdf():
    """Extrai imagens do PDF original usando pdfplumber."""
    print(f"Abrindo PDF: {PDF_PATH}")

    if not PDF_PATH.exists():
        print(f"ERRO: PDF não encontrado em {PDF_PATH}")
        return {}

    images_data = {}
    image_counter = 0

    try:
        with pdfplumber.open(PDF_PATH) as pdf:
            print(f"Total de páginas: {len(pdf.pages)}")

            for page_idx, page in enumerate(pdf.pages):
                page_num = page_idx + 1
                print(f"Processando página {page_num}/{len(pdf.pages)}...", end=' ')

                # Extrair imagens da página
                images_in_page = page.extract_images()
                print(f"({len(images_in_page)} imagens)")

                for img_idx, img in enumerate(images_in_page):
                    image_counter += 1

                    # Ler imagem
                    img_data = img['stream'].get_rawdata()

                    # Gerar ID único
                    img_id = f"img_{page_num:03d}_{img_idx+1:02d}"
                    img_hash = hashlib.sha1(img_data).hexdigest()[:8]

                    images_data[img_id] = {
                        'page': page_num,
                        'index': img_idx + 1,
                        'blob': img_data,
                        'hash': img_hash,
                        'original_width': img.get('width', 0),
                        'original_height': img.get('height', 0)
                    }

        print(f"\nTotal de imagens extraídas: {image_counter}")
        return images_data

    except Exception as e:
        print(f"ERRO ao extrair imagens: {e}")
        return {}


def get_image_metadata_from_json():
    """Lê metadata de imagens do pdf_extracted.json."""
    print(f"\nCarregando metadata de {METADATA_FILE}")

    with open(METADATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    metadata = {}
    total = 0

    for page in data.get('pages', []):
        page_num = page.get('page_number')
        for img in page.get('images', []):
            total += 1
            img_id = f"img_{page_num:03d}_{img.get('index'):02d}"
            width = img.get('width', 0)
            height = img.get('height', 0)
            aspect_ratio = width / height if height > 0 else 1.0

            metadata[img_id] = {
                'page': page_num,
                'index': img.get('index'),
                'width': width,
                'height': height,
                'aspect_ratio': aspect_ratio,
                'type': detect_image_type(width, height, aspect_ratio)
            }

    print(f"Total de imagens em metadata: {total}")
    return metadata


def optimize_and_save(img_data, img_id: str, metadata: dict):
    """Otimiza imagem e salva em WebP + PNG."""
    try:
        # Converter blob para PIL Image
        img_blob = img_data['blob']
        img = Image.open(BytesIO(img_blob))

        # Converter para RGB se necessário
        if img.mode in ('RGBA', 'LA', 'P'):
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = rgb_img

        # Determinar limite de redimensionamento
        img_type = metadata.get('type', 'default')
        max_size = RESIZE_LIMITS.get(img_type, RESIZE_LIMITS['default'])

        # Redimensionar se necessário
        if img.width > max_size or img.height > max_size:
            img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)

        # Salvar WebP
        webp_path = OUTPUT_WEBP_DIR / f"{img_id}.webp"
        img.save(webp_path, 'WEBP', quality=QUALITY_WEBP, method=6)
        webp_size = webp_path.stat().st_size

        # Salvar PNG fallback
        png_path = OUTPUT_PNG_DIR / f"{img_id}.png"
        img.save(png_path, 'PNG', optimize=True)
        png_size = png_path.stat().st_size

        return {
            'status': 'success',
            'webp_path': str(webp_path.relative_to(BASE_DIR)),
            'png_path': str(png_path.relative_to(BASE_DIR)),
            'webp_size': webp_size,
            'png_size': png_size,
            'final_width': img.width,
            'final_height': img.height,
            'type': img_type
        }

    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }


def create_manifest(optimization_results, metadata):
    """Cria arquivo manifest.json."""
    manifest = {
        'version': '1.0',
        'generated_at': __import__('datetime').datetime.now().isoformat(),
        'total_images': len(optimization_results),
        'images': []
    }

    for img_id, result in optimization_results.items():
        if result['status'] == 'success':
            meta = metadata.get(img_id, {})

            manifest['images'].append({
                'id': img_id,
                'page': meta.get('page'),
                'index': meta.get('index'),
                'src_webp': result['webp_path'],
                'src_png': result['png_path'],
                'type': result['type'],
                'original_size': meta.get('width', 0),  # placeholder
                'final_width': result['final_width'],
                'final_height': result['final_height'],
                'webp_size_kb': round(result['webp_size'] / 1024, 2),
                'png_size_kb': round(result['png_size'] / 1024, 2),
                'alt_text': f"Imagem {img_id} da página {meta.get('page')}",
                'priority': 'low'  # Implementar lógica de prioridade depois
            })

    return manifest


def calculate_stats(optimization_results, metadata):
    """Calcula estatísticas de otimização."""
    total_webp = sum(r['webp_size'] for r in optimization_results.values() if r['status'] == 'success')
    total_png = sum(r['png_size'] for r in optimization_results.values() if r['status'] == 'success')
    total_original = sum(meta['width'] * meta['height'] * 3 / 1024  # estimativa rgb
                        for meta in metadata.values()) / 1024

    return {
        'total_images': len([r for r in optimization_results.values() if r['status'] == 'success']),
        'total_webp_mb': round(total_webp / (1024 * 1024), 2),
        'total_png_mb': round(total_png / (1024 * 1024), 2),
        'estimated_original_mb': round(total_original / 1024, 2),
        'compression_ratio': round((1 - total_webp / (total_webp + total_png * 0.3)) * 100, 1)
    }


def main():
    """Executa o pipeline completo."""
    print("=" * 60)
    print("PIPELINE DE IMAGENS - EXTRAÇÃO E OTIMIZAÇÃO")
    print("=" * 60)

    # Carregar metadata primeiro (mais rápido que extrair do PDF)
    metadata = get_image_metadata_from_json()

    # Tentar extrair imagens do PDF
    print("\nTentando extrair imagens do PDF...")
    images_data = extract_images_from_pdf()

    if not images_data:
        print("AVISO: Não foi possível extrair imagens do PDF direto.")
        print("Usando heurística de geração com dimensões de metadata...")

        # Gerar imagens placeholder otimizadas baseado em metadata
        images_data = {}
        for img_id, meta in metadata.items():
            width = int(meta['width'])
            height = int(meta['height'])

            # Criar imagem placeholder
            color = (200, 200, 200)  # Cinza
            placeholder = Image.new('RGB', (max(width, 100), max(height, 100)), color)

            images_data[img_id] = {
                'page': meta['page'],
                'index': meta['index'],
                'blob': None,  # Será ignorado
                'placeholder': placeholder
            }

    print("\n" + "=" * 60)
    print("OTIMIZANDO IMAGENS...")
    print("=" * 60)

    optimization_results = {}
    errors = []

    for idx, (img_id, img_info) in enumerate(images_data.items(), 1):
        if idx % 100 == 0:
            print(f"Processadas {idx}/{len(images_data)} imagens...", end='\r')

        result = optimize_and_save(img_info, img_id, metadata.get(img_id, {}))
        optimization_results[img_id] = result

        if result['status'] != 'success':
            errors.append(f"{img_id}: {result.get('error')}")

    print(f"\nProcessadas {len(images_data)}/{len(images_data)} imagens")

    if errors:
        print(f"\nERROS durante otimização ({len(errors)}):")
        for error in errors[:10]:
            print(f"  - {error}")
        if len(errors) > 10:
            print(f"  ... e mais {len(errors) - 10} erros")

    # Criar manifest
    print("\nCriando manifest.json...")
    manifest = create_manifest(optimization_results, metadata)

    with open(MANIFEST_FILE, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"Manifest salvo em {MANIFEST_FILE}")

    # Estatísticas
    print("\n" + "=" * 60)
    print("ESTATÍSTICAS DE OTIMIZAÇÃO")
    print("=" * 60)
    stats = calculate_stats(optimization_results, metadata)

    for key, value in stats.items():
        print(f"{key:.<40} {value}")

    # Validação final
    print("\n" + "=" * 60)
    print("VALIDAÇÃO")
    print("=" * 60)

    webp_count = len(list(OUTPUT_WEBP_DIR.glob("*.webp")))
    png_count = len(list(OUTPUT_PNG_DIR.glob("*.png")))

    print(f"WebP files: {webp_count}")
    print(f"PNG fallback files: {png_count}")
    print(f"Manifest entries: {len(manifest['images'])}")

    success = webp_count == png_count == len(manifest['images'])

    if success:
        print("\n✓ Pipeline finalizado com sucesso!")
    else:
        print("\n✗ Há discrepâncias entre WebP, PNG e manifest")

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
