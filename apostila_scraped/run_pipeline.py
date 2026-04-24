#!/usr/bin/env python3
"""
Script de execução do pipeline de imagens
- Verifica dependências
- Executa pipeline_images.py
- Gera relatório de execução
"""

import sys
import subprocess
from pathlib import Path
import json

def check_dependencies():
    """Verifica se as bibliotecas necessárias estão instaladas."""
    print("Verificando dependências...")

    required = {
        'pdfplumber': 'pdfplumber',
        'PIL': 'pillow',
        'json': 'json'  # Built-in
    }

    missing = []

    for import_name, package_name in required.items():
        if import_name == 'json':
            continue  # Built-in

        try:
            __import__(import_name)
            print(f"  ✓ {package_name}")
        except ImportError:
            print(f"  ✗ {package_name}")
            missing.append(package_name)

    if missing:
        print(f"\nInstalando pacotes faltantes: {', '.join(missing)}")
        for pkg in missing:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', pkg])
        print("Pacotes instalados com sucesso!")

    return len(missing) == 0


def run_pipeline():
    """Executa o pipeline de imagens."""
    script_path = Path(__file__).parent / "pipeline_images.py"

    if not script_path.exists():
        print(f"ERRO: {script_path} não encontrado")
        return False

    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=False,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        print(f"ERRO ao executar pipeline: {e}")
        return False


def main():
    print("=" * 60)
    print("PIPELINE DE OTIMIZAÇÃO DE IMAGENS")
    print("=" * 60)
    print()

    # Verificar dependências
    if not check_dependencies():
        print("Erro: Dependências não puderam ser instaladas")
        return 1

    print()

    # Executar pipeline
    if not run_pipeline():
        print("Erro: Pipeline falhou")
        return 1

    print()
    print("=" * 60)
    print("PIPELINE FINALIZADO COM SUCESSO")
    print("=" * 60)

    return 0


if __name__ == '__main__':
    sys.exit(main())
