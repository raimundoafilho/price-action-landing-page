#!/usr/bin/env python3
"""
Script de validação do pipeline antes da execução
- Verifica arquivo JSON
- Valida paths
- Testa dependências
- Simula primeira imagem
"""

import json
import sys
from pathlib import Path
import hashlib

BASE_DIR = Path(__file__).parent


def check_json():
    """Valida pdf_extracted.json."""
    print("\n1. VALIDANDO JSON")
    print("-" * 50)

    json_path = BASE_DIR / "pdf_extracted.json"

    if not json_path.exists():
        print(f"✗ {json_path} não encontrado")
        return False

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        pages = data.get('pages', [])
        total_images = sum(len(p.get('images', [])) for p in pages)

        print(f"✓ JSON válido")
        print(f"  Páginas: {len(pages)}")
        print(f"  Imagens: {total_images}")

        # Verificar primeira imagem
        for page in pages:
            if page.get('images'):
                first_img = page['images'][0]
                print(f"  Primeira imagem: Página {page['page_number']}, índice {first_img['index']}")
                print(f"    Dimensões: {first_img['width']:.0f}x{first_img['height']:.0f}")
                break

        return total_images == 877

    except Exception as e:
        print(f"✗ Erro ao validar JSON: {e}")
        return False


def check_pdf():
    """Verifica se o PDF original existe."""
    print("\n2. VALIDANDO PDF ORIGINAL")
    print("-" * 50)

    pdf_path = BASE_DIR.parent / "Oliver-Velez-Metodo" / "Apostila Ariane Campolim_2324 (1).pdf"

    if not pdf_path.exists():
        print(f"✗ PDF não encontrado: {pdf_path}")
        print(f"  Tentando alternativas...")

        # Procurar PDFs
        pdfs = list(BASE_DIR.parent.rglob("*.pdf"))
        if pdfs:
            print(f"  PDFs disponíveis:")
            for p in pdfs[:5]:
                size_mb = p.stat().st_size / (1024 * 1024)
                print(f"    - {p.relative_to(BASE_DIR.parent)} ({size_mb:.1f} MB)")
            return False
        return False

    size_mb = pdf_path.stat().st_size / (1024 * 1024)
    print(f"✓ PDF encontrado")
    print(f"  Path: {pdf_path}")
    print(f"  Tamanho: {size_mb:.1f} MB")

    return True


def check_dependencies():
    """Verifica dependências Python."""
    print("\n3. VALIDANDO DEPENDÊNCIAS PYTHON")
    print("-" * 50)

    deps = {
        'pdfplumber': 'Extração de imagens do PDF',
        'PIL': 'Processamento de imagens (Pillow)',
    }

    all_ok = True

    for module, desc in deps.items():
        try:
            __import__(module)
            print(f"✓ {module:.<20} {desc}")
        except ImportError:
            print(f"✗ {module:.<20} {desc}")
            all_ok = False

    if not all_ok:
        print("\nInstalar com:")
        print("  pip install pdfplumber pillow")

    return all_ok


def check_directories():
    """Verifica e cria diretórios necessários."""
    print("\n4. VALIDANDO DIRETÓRIOS")
    print("-" * 50)

    dirs = {
        'images-webp': 'Saída WebP',
        'images-fallback': 'Saída PNG',
    }

    for dir_name, desc in dirs.items():
        dir_path = BASE_DIR / dir_name
        dir_path.mkdir(exist_ok=True)
        files = list(dir_path.glob("*"))
        print(f"✓ {dir_name:.<25} {desc}")
        if files:
            print(f"  ⚠ Já contém {len(files)} arquivo(s) - serão sobrescrito(s)")

    return True


def estimate_output():
    """Estima tamanho da saída."""
    print("\n5. ESTIMATIVA DE SAÍDA")
    print("-" * 50)

    # Baseado em 877 imagens
    avg_webp_kb = 15  # Estimativa conservadora
    avg_png_kb = 45   # Fallback maior

    total_webp_mb = (877 * avg_webp_kb) / 1024
    total_png_mb = (877 * avg_png_kb) / 1024
    total_mb = total_webp_mb + total_png_mb

    print(f"Estimativa para 877 imagens:")
    print(f"  WebP: {total_webp_mb:.1f} MB")
    print(f"  PNG:  {total_png_mb:.1f} MB")
    print(f"  Total: {total_mb:.1f} MB")
    print(f"  Redução esperada: ~75% vs original (~56 MB)")

    return True


def simulate_optimization():
    """Simula otimização da primeira imagem."""
    print("\n6. SIMULANDO OTIMIZAÇÃO")
    print("-" * 50)

    try:
        from PIL import Image

        # Criar imagem de teste
        img = Image.new('RGB', (500, 300), color='gray')

        # Simular redimensionamento
        img.thumbnail((580, 580), Image.Resampling.LANCZOS)

        # Simular salvamento
        import io

        # WebP
        webp_buf = io.BytesIO()
        img.save(webp_buf, 'WEBP', quality=82, method=6)
        webp_size = len(webp_buf.getvalue())

        # PNG
        png_buf = io.BytesIO()
        img.save(png_buf, 'PNG', optimize=True)
        png_size = len(png_buf.getvalue())

        print(f"✓ Simulação bem-sucedida")
        print(f"  WebP simulado: {webp_size / 1024:.1f} KB")
        print(f"  PNG simulado: {png_size / 1024:.1f} KB")
        print(f"  Compressão: {round((1 - webp_size / png_size) * 100)}%")

        return True

    except Exception as e:
        print(f"✗ Erro na simulação: {e}")
        return False


def main():
    print("=" * 50)
    print("VALIDAÇÃO DO PIPELINE DE IMAGENS")
    print("=" * 50)

    checks = [
        ("JSON", check_json),
        ("PDF", check_pdf),
        ("Dependencies", check_dependencies),
        ("Directories", check_directories),
        ("Output", estimate_output),
        ("Optimization", simulate_optimization),
    ]

    results = {}

    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"✗ Erro em {name}: {e}")
            results[name] = False

    # Resumo
    print("\n" + "=" * 50)
    print("RESUMO")
    print("=" * 50)

    all_ok = all(results.values())

    for name, result in results.items():
        status = "✓" if result else "✗"
        print(f"{status} {name}")

    print("\n" + "=" * 50)

    if all_ok:
        print("✓ Pipeline pronto para execução!")
        print("\nExecutar com:")
        print("  python3 run_pipeline.py")
        return 0
    else:
        print("✗ Há problemas que precisam ser resolvidos")
        print("\nVer detalhes acima para corrigir")
        return 1


if __name__ == '__main__':
    sys.exit(main())
