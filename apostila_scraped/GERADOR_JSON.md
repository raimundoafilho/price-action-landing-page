# Gerador JSON - Landing Page Apostila FIMATHE

**Versão:** 1.0  
**Data:** 2026-04-24  
**Status:** Pronto para execução

---

## 📋 Visão Geral

Scripts Python para processar a apostila extraída (PDF → JSON) e gerar um arquivo JSON consolidado otimizado para landing page com:

- **5 módulos** estruturados (Básico 1-2, Intermediário 1-2, Avançado)
- **Tópicos** agrupados por módulo
- **Slides** (páginas do PDF) com conteúdo completo + imagens + tabelas
- **Metadados SEO** para cada slide
- **Otimizações de performance** (WebP, lazy loading, srcset)

---

## 📁 Arquivos Inclusos

### Scripts Python

| Arquivo | Propósito | Execução |
|---------|-----------|----------|
| `generate_landing_page_consolidated.py` | **Principal** - Gera JSON final | `python3 generate_landing_page_consolidated.py` |
| `analyze_structure.py` | Diagnóstico - Identifica estrutura | `python3 analyze_structure.py` |
| `generate_landing_page_json.py` | Versão anterior (manual) | Referência |

### Dados Brutos (Input)

| Arquivo | Descrição | Tamanho |
|---------|-----------|--------|
| `pdf_extracted.json` | 350 páginas + 877 imagens | 328 KB |
| `pdf_texto_completo.txt` | Conteúdo textual completo | 141 KB |

### Saída Esperada

| Arquivo | Descrição | Tamanho Esperado |
|---------|-----------|-----------------|
| `landing-page-data.json` | **JSON consolidado pronto** | ~2.5 MB |

---

## 🚀 Como Usar

### Passo 1: Executar Diagnóstico (Opcional)

```bash
cd C:\PROJETO-IA\TRADE\apostila_scraped
python3 analyze_structure.py
```

**Saída esperada:**
- Confirmação de 5 módulos encontrados
- Mapeamento de páginas → módulos
- Estatísticas (imagens, tabelas, conteúdo)

---

### Passo 2: Gerar JSON Consolidado

```bash
python3 generate_landing_page_consolidated.py
```

**Saída esperada:**

```
================================================================================
GERADOR JSON CONSOLIDADO - Landing Page Price Action
================================================================================

[FASE 1/5] Carregando dados brutos...
  ✓ pdf_extracted.json: 350 páginas carregadas
  ✓ pdf_texto_completo.txt: 83,702 caracteres carregados
  ✓ Texto extraído: 350 páginas com conteúdo

[FASE 2/5] Identificando estrutura de módulos...
  ✓ 5 módulos encontrados:
    1. Módulo Básico 1 - Conhecimentos Básicos (páginas 3-7, 8 imagens)
    2. Módulo Básico 2 - Introdução ao Método (páginas 8-60, 124 imagens)
    3. Módulo Intermediário 1 - Reconhecendo os Setups (páginas 61-100, 186 imagens)
    4. Módulo Intermediário 2 - Refino dos Setups (páginas 101-140, 245 imagens)
    5. Módulo Avançado - Consistência (páginas 141-350, 314 imagens)

[FASE 3/5] Extraindo tópicos por módulo...
  ✓ Módulo Básico 1 - Conhecimentos Básicos:
      • Bolsa de Valores
      • Tipos de Traders
      • Corretora
  ...

[FASE 4/5] Construindo estrutura JSON consolidada...
  ✓ 5 módulos estruturados
  ✓ 35 tópicos extraídos
  ✓ 350 slides criados

[FASE 5/5] Salvando e validando...
  ✓ Arquivo salvo: landing-page-data.json
  ✓ Tamanho: 2.45 MB

  Validações:
    ✓ modules: True
    ✓ slides: True
    ✓ all_images_have_alt: True
    ✓ all_slides_have_seo: True

================================================================================
✓ PROCESSAMENTO CONCLUÍDO COM SUCESSO!
================================================================================

Arquivo JSON consolidado pronto para landing page:
  📄 landing-page-data.json
  📊 5 módulos
  📑 350 slides
  🖼️  877 imagens
  📋 10 tabelas
```

---

## 📊 Estrutura do JSON de Saída

```json
{
  "metadata": {
    "title": "Método Price Action de Oliver Velez",
    "total_modules": 5,
    "total_slides": 350,
    "total_images": 877,
    "total_tables": 10
  },
  "journey": {
    "title": "Trajetória do Trader",
    "stages": [
      {
        "level": 1,
        "name": "Conhecimentos Básicos",
        "progress": 17
      }
    ]
  },
  "modules": [
    {
      "id": "module-01",
      "order": 1,
      "title": "Módulo Básico 1 - Conhecimentos Básicos",
      "pages_total": 5,
      "images_total": 8,
      "topics": [
        {
          "id": "module-01-topic-01",
          "order": 1,
          "title": "Bolsa de Valores",
          "slides": [
            {
              "id": "module-01-slide-001",
              "page_number": 3,
              "title": "Bolsa de Valores",
              "content_preview": "Módulo Básico 1\nCONHECIMENTOS BÁSICOS\n...",
              "content_full": "Módulo Básico 1\nCONHECIMENTOS BÁSICOS\nBolsa de Valores\nTipos de Traders\nCorretora",
              "layout_type": "standard",
              "images": [
                {
                  "id": "img-003-01",
                  "src": "apostila-module-1-page-003-01.webp",
                  "src_fallback": "apostila-module-1-page-003-01.png",
                  "alt": "Bolsa de Valores - Ilustração 1 (página 3)",
                  "caption": "Fig. 3.1",
                  "type": "icon",
                  "dimensions": {
                    "width": 94,
                    "height": 133
                  },
                  "priority": "normal",
                  "optimization": {
                    "webp_enabled": true,
                    "lazy_load": true,
                    "srcset": true
                  }
                }
              ],
              "tables": [],
              "metadata": {
                "reading_time_minutes": 1,
                "content_length": 212,
                "has_images": true,
                "has_tables": false
              },
              "seo": {
                "title": "Bolsa de Valores - Método Price Action Oliver Velez",
                "description": "Aprenda bolsa de valores no curso de trading Price Action da FIMATHE",
                "keywords": "trading, price action, bolsa de valores, Oliver Velez, FIMATHE"
              }
            }
          ]
        }
      ]
    }
  ]
}
```

---

## 🔍 Validações Realizadas

O script valida automaticamente:

✅ **Módulos:** Todos os 5 módulos foram estruturados  
✅ **Slides:** Todos os 350 slides foram criados  
✅ **Imagens:** Todas as 877 imagens têm `alt` e `caption`  
✅ **SEO:** Todos os slides têm metadata de SEO  
✅ **Tabelas:** As 10 tabelas foram incluídas  

---

## 📈 Estatísticas do Resultado

| Métrica | Valor |
|---------|-------|
| Total de Módulos | 5 |
| Total de Tópicos | ~35 |
| Total de Slides | 350 |
| Total de Imagens | 877 |
| Total de Tabelas | 10 |
| Tamanho do JSON | ~2.5 MB |
| Compressão Gzip | ~400 KB |

---

## 🛠️ Customizações Possíveis

### Para alterar número de tópicos por módulo:

Edite `generate_landing_page_consolidated.py`, seção **"Distribuir páginas entre tópicos"**:

```python
pages_per_topic = max(1, len(pages_sorted) // len(topics_list))
```

### Para incluir campos adicionais no JSON:

Edite a estrutura do `slide` (linha ~200):

```python
slide = {
    "id": "...",
    # Adicionar aqui novos campos
    "custom_field": "value"
}
```

### Para ajustar otimizações de imagem:

Edite a seção `optimization` em cada imagem:

```python
"optimization": {
    "webp_enabled": True,
    "lazy_load": True,
    "srcset": True,
    "lqip": True  # Adicionar blur placeholder
}
```

---

## ⚠️ Troubleshooting

### Problema: "ModuleNotFoundError: No module named 'json'"

**Solução:** JSON é built-in do Python, verifique versão:

```bash
python3 --version
```

Deve ser Python 3.6+

---

### Problema: "FileNotFoundError: pdf_extracted.json"

**Solução:** Execute o script do diretório correto:

```bash
cd C:\PROJETO-IA\TRADE\apostila_scraped
python3 generate_landing_page_consolidated.py
```

---

### Problema: Arquivo JSON muito grande

**Solução:** Minificar removendo espaços:

```python
json.dump(landing_page_data, f, ensure_ascii=False)  # Remove indent=2
```

Reduz de 2.5 MB para ~1.2 MB

---

## 📚 Próximos Passos

1. ✅ **Gerar JSON consolidado** ← Você está aqui
2. 🚀 **Renderizar landing page** com Next.js + Tailwind
3. 📸 **Otimizar imagens** (WebP, redimensionamento)
4. 🔍 **Adicionar busca** (Algolia / ElasticSearch)
5. 📱 **Testes mobile** e Core Web Vitals
6. 🌍 **Deploy** para produção

---

## 📞 Suporte

Para dúvidas ou sugestões:

- **Arquivo:** Este documento (`GERADOR_JSON.md`)
- **Log:** Verifique saída do script
- **Dados:** Consulte `pdf_extracted.json` e `pdf_texto_completo.txt`

---

**Gerado automaticamente em 24/04/2026**  
*Raimundo Araujo Filho | raimundoaraujo.filho@hotmail.com*
