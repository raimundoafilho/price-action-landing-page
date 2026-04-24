#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PDF to Landing Page Converter
Converte PDF (Trading) → Landing Page HTML profissional
Com suporte a texto, tabelas e imagens

Uso: python pdf-to-landing-page.py seu_arquivo.pdf
"""

import sys
import os
from pathlib import Path
import pdfplumber
from jinja2 import Template
from datetime import datetime

# Cores para terminal
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_status(msg, status="info"):
    """Print com cores"""
    if status == "success":
        print(f"{Colors.OKGREEN}✓ {msg}{Colors.ENDC}")
    elif status == "error":
        print(f"{Colors.FAIL}✗ {msg}{Colors.ENDC}")
    elif status == "warning":
        print(f"{Colors.WARNING}⚠ {msg}{Colors.ENDC}")
    else:
        print(f"{Colors.OKBLUE}ℹ {msg}{Colors.ENDC}")

def extract_pdf_content(pdf_path):
    """Extrai texto, tabelas e metadados do PDF"""
    print_status(f"Lendo PDF: {pdf_path}", "info")

    content = {
        'pages': [],
        'total_pages': 0,
        'title': os.path.basename(pdf_path),
        'extracted_at': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }

    try:
        with pdfplumber.open(pdf_path) as pdf:
            content['total_pages'] = len(pdf.pages)
            print_status(f"Total de páginas: {content['total_pages']}", "success")

            for page_num, page in enumerate(pdf.pages, 1):
                page_content = {
                    'number': page_num,
                    'text': page.extract_text() or '',
                    'tables': page.extract_tables() or []
                }

                # Extrair informações de estrutura (headings)
                text = page_content['text']
                lines = text.split('\n') if text else []

                # Dividir em seções (simples heurística)
                page_content['sections'] = []
                current_section = None

                for line in lines:
                    if line.strip():
                        # Linhas em CAPS LOCK são potenciais headings
                        if line.isupper() and len(line) > 3:
                            if current_section:
                                page_content['sections'].append(current_section)
                            current_section = {
                                'title': line.strip(),
                                'content': []
                            }
                        elif current_section:
                            current_section['content'].append(line.strip())

                if current_section:
                    page_content['sections'].append(current_section)

                content['pages'].append(page_content)
                print_status(f"Página {page_num} extraída", "success")

    except Exception as e:
        print_status(f"Erro ao ler PDF: {e}", "error")
        raise

    return content

def create_html_template():
    """Cria template HTML profissional"""
    html_template = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} — Landing Page</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --primary: #1a3a52;
            --secondary: #2d5f8d;
            --accent: #f39c12;
            --text: #2c3e50;
            --bg: #f8f9fa;
            --border: #e0e0e0;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg);
            color: var(--text);
            line-height: 1.7;
        }

        header {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            padding: 3rem 2rem;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        header h1 {
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }

        section {
            background: white;
            border-radius: 8px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid var(--accent);
        }

        h2 {
            color: var(--primary);
            font-size: 1.8rem;
            margin-bottom: 1rem;
            border-bottom: 2px solid var(--accent);
            padding-bottom: 0.5rem;
        }

        h3 {
            color: var(--secondary);
            font-size: 1.3rem;
            margin-top: 1.5rem;
            margin-bottom: 0.75rem;
        }

        p {
            margin-bottom: 1rem;
            color: #555;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
            background: white;
        }

        th {
            background-color: var(--primary);
            color: white;
            padding: 1rem;
            text-align: left;
            font-weight: 600;
        }

        td {
            padding: 0.75rem 1rem;
            border-bottom: 1px solid var(--border);
        }

        tr:hover {
            background-color: rgba(243, 156, 18, 0.05);
        }

        ul, ol {
            margin-left: 2rem;
            margin-bottom: 1rem;
        }

        li {
            margin-bottom: 0.5rem;
        }

        .highlight {
            background-color: #fff3cd;
            border-left: 4px solid var(--accent);
            padding: 1rem;
            border-radius: 4px;
            margin: 1.5rem 0;
        }

        .info-box {
            background-color: #e7f3ff;
            border-left: 4px solid var(--secondary);
            padding: 1rem;
            border-radius: 4px;
            margin: 1.5rem 0;
        }

        footer {
            background: var(--primary);
            color: white;
            text-align: center;
            padding: 2rem;
            margin-top: 3rem;
        }

        code {
            background-color: #f4f4f4;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            color: #d63384;
        }

        pre {
            background-color: #f4f4f4;
            padding: 1rem;
            border-radius: 4px;
            overflow-x: auto;
            margin: 1rem 0;
        }

        .meta-info {
            color: #999;
            font-size: 0.9rem;
            text-align: center;
            margin-bottom: 2rem;
        }

        @media (max-width: 768px) {
            header h1 {
                font-size: 1.8rem;
            }

            section {
                padding: 1.5rem;
            }

            h2 {
                font-size: 1.4rem;
            }

            .container {
                padding: 1rem;
            }

            table {
                font-size: 0.9rem;
            }

            th, td {
                padding: 0.5rem;
            }
        }
    </style>
</head>
<body>
    <header>
        <h1>📄 {{ title }}</h1>
        <p>Landing page extraída de PDF</p>
    </header>

    <div class="meta-info">
        <p>Extraído em {{ extracted_at }} | Total de {{ total_pages }} páginas</p>
    </div>

    <div class="container">
        {% for page in pages %}
            <section id="page-{{ page.number }}">
                <h2>Página {{ page.number }}</h2>

                {% if page.sections %}
                    {% for section in page.sections %}
                        <h3>{{ section.title }}</h3>
                        <div>
                            {% for content_line in section.content %}
                                <p>{{ content_line }}</p>
                            {% endfor %}
                        </div>
                    {% endfor %}
                {% else %}
                    <div class="info-box">
                        <p>{{ page.text }}</p>
                    </div>
                {% endif %}

                {% if page.tables %}
                    <h3>Tabelas encontradas:</h3>
                    {% for table in page.tables %}
                        <table>
                            {% for row in table %}
                                <tr>
                                    {% for cell in row %}
                                        <td>{{ cell or '-' }}</td>
                                    {% endfor %}
                                </tr>
                            {% endfor %}
                        </table>
                    {% endfor %}
                {% endif %}
            </section>
        {% endfor %}
    </div>

    <footer>
        <p><strong>Landing Page Automática</strong></p>
        <p>Criada a partir de PDF em {{ extracted_at }}</p>
        <p style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.8;">
            Use este arquivo como base e customize conforme necessário.
        </p>
    </footer>
</body>
</html>"""
    return html_template

def generate_landing_page(pdf_path, output_path=None):
    """Converte PDF em landing page HTML"""

    # Validar arquivo
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        print_status(f"Arquivo não encontrado: {pdf_path}", "error")
        sys.exit(1)

    if not pdf_path.suffix.lower() == '.pdf':
        print_status(f"Arquivo não é PDF: {pdf_path}", "error")
        sys.exit(1)

    # Determinar caminho de saída
    if output_path is None:
        output_path = pdf_path.stem + '_landing_page.html'

    print_status(f"Iniciando conversão...", "info")
    print_status(f"Entrada: {pdf_path}", "info")
    print_status(f"Saída: {output_path}", "info")
    print()

    try:
        # Extrair conteúdo
        content = extract_pdf_content(str(pdf_path))
        print()

        # Criar template
        print_status("Criando template HTML...", "info")
        html_template = create_html_template()
        template = Template(html_template)
        print_status("Template criado com sucesso", "success")

        # Renderizar
        print_status("Renderizando landing page...", "info")
        html_content = template.render(**content)
        print_status("Renderização concluída", "success")

        # Salvar
        print_status(f"Salvando em: {output_path}", "info")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print_status(f"Landing page salva com sucesso!", "success")

        print()
        print(f"{Colors.OKGREEN}{Colors.BOLD}✓ Conversão concluída com sucesso!{Colors.ENDC}")
        print(f"{Colors.BOLD}Abra em navegador: {output_path}{Colors.ENDC}")

        return output_path

    except Exception as e:
        print_status(f"Erro durante conversão: {e}", "error")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def main():
    """Função principal"""
    print()
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("╔════════════════════════════════════════╗")
    print("║   PDF to Landing Page Converter       ║")
    print("║   Converte PDF → HTML profissional    ║")
    print("╚════════════════════════════════════════╝")
    print(f"{Colors.ENDC}")
    print()

    if len(sys.argv) < 2:
        print(f"{Colors.WARNING}Uso: python pdf-to-landing-page.py <arquivo.pdf> [output.html]{Colors.ENDC}")
        print()
        print("Exemplos:")
        print("  python pdf-to-landing-page.py trading.pdf")
        print("  python pdf-to-landing-page.py trading.pdf resultado.html")
        print()
        sys.exit(1)

    pdf_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    generate_landing_page(pdf_file, output_file)

if __name__ == '__main__':
    main()
