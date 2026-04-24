#!/bin/bash
# COMANDOS ESSENCIAIS - Gerador JSON Consolidado
# Data: 2026-04-24
# Projeto: Apostila FIMATHE - Método Price Action

echo "═══════════════════════════════════════════════════════════════════════════════"
echo "COMANDOS ESSENCIAIS - Gerador JSON Consolidado"
echo "═══════════════════════════════════════════════════════════════════════════════"

# ═════════════════════════════════════════════════════════════════════════════════
# PASSO 1: VALIDAÇÃO DO AMBIENTE
# ═════════════════════════════════════════════════════════════════════════════════

echo ""
echo "[PASSO 1] Validando Ambiente..."
echo "───────────────────────────────────────────────────────────────────────────────"

# Verificar Python
echo "Verificando Python 3..."
python3 --version

# Verificar diretório
echo ""
echo "Verificando diretório atual..."
pwd

# Verificar arquivos de entrada
echo ""
echo "Verificando arquivos de entrada..."
ls -lh pdf_extracted.json pdf_texto_completo.txt

# ═════════════════════════════════════════════════════════════════════════════════
# PASSO 2: EXECUTAR SCRIPT PRINCIPAL
# ═════════════════════════════════════════════════════════════════════════════════

echo ""
echo "[PASSO 2] Executando Script Principal..."
echo "───────────────────────────────────────────────────────────────────────────────"

python3 generate_landing_page_consolidated.py

# ═════════════════════════════════════════════════════════════════════════════════
# PASSO 3: VALIDAR SAÍDA
# ═════════════════════════════════════════════════════════════════════════════════

echo ""
echo "[PASSO 3] Validando Arquivo de Saída..."
echo "───────────────────────────────────────────────────────────────────────────────"

# Verificar se arquivo foi criado
echo "Verificando se landing-page-data.json foi criado..."
ls -lh landing-page-data.json

# Validar JSON
echo ""
echo "Validando sintaxe JSON..."
python3 -m json.tool landing-page-data.json > /dev/null && echo "✓ JSON válido!" || echo "✗ JSON inválido!"

# Contar módulos
echo ""
echo "Contando módulos..."
grep -c '"id": "module-' landing-page-data.json

# Contar tópicos
echo ""
echo "Contando tópicos..."
grep -c '"id": "module-[0-9]*-topic-' landing-page-data.json

# Contar slides
echo ""
echo "Contando slides..."
grep -c '"page_number":' landing-page-data.json

# Contar imagens
echo ""
echo "Contando imagens..."
grep -c '"id": "img-' landing-page-data.json

# ═════════════════════════════════════════════════════════════════════════════════
# PASSO 4: RELATÓRIO FINAL
# ═════════════════════════════════════════════════════════════════════════════════

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "✓ PROCESSAMENTO COMPLETO!"
echo "═══════════════════════════════════════════════════════════════════════════════"

echo ""
echo "Próximos Passos:"
echo "  1. Fazer backup: cp landing-page-data.json landing-page-data-backup.json"
echo "  2. Copiar para Next.js: cp landing-page-data.json ../squads/price-action-education/public/data/"
echo "  3. Testar em navegador"
echo "  4. Deploy para produção"

echo ""
echo "Suporte: raimundoaraujo.filho@hotmail.com"
echo ""
