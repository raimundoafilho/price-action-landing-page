# 🎯 PLANO DE RESGATE - OPÇÃO B (LANDING PAGE ILUSTRADA)

## STATUS ATUAL (2026-04-24 23:XX)

### ✅ JÁ FEITO
- [x] Landing page HTML/CSS/JS funciona (login, sidebar, navegação)
- [x] PDF 350 páginas analisado completo
- [x] Estrutura real do PDF mapeada (5 módulos, 25+ seções)
- [x] 877 imagens metadados no pdf_extracted.json (localizações preservadas)
- [x] Código GitHub sincronizado

### ❌ AINDA FALTA
- [ ] Extrair imagens do PDF original (Ariane Campolim_2324.pdf)
- [ ] Renomear/organizar imagens por página+seção
- [ ] Criar JSON de mapeamento (page → image)
- [ ] Integrar imagens ao HTML/JS da landing page
- [ ] Limpar metadata (remover "Ariane", números de página, etc)
- [ ] Teste end-to-end (local + GitHub Pages)

---

## PRÓXIMOS PASSOS (QUANDO TOKENS RESETAREM)

### PASSO 1: EXTRAIR IMAGENS DO PDF (45 min)
```bash
# Localização do PDF original:
C:\PROJETO-IA\TRADE\Oliver-Velez-Metodo\Apostila Ariane Campolim_2324 (1).pdf

# Usar PyPDF2 + Pillow para:
# 1. Ler cada página do PDF
# 2. Extrair imagens de cada página
# 3. Salvar em: apostila_scraped/images/{page_number}/
# 4. Renomear: page_003_img_01.png, page_003_img_02.png, etc

# Resultado esperado: ~877 arquivos PNG/JPEG
```

### PASSO 2: CRIAR MAPEAMENTO JSON (15 min)
```json
{
  "page_3": [
    {"image_id": "pg_003_img_01", "file": "apostila_scraped/images/page_003/img_01.png", "section": "Bolsa de Valores"},
    {"image_id": "pg_003_img_02", "file": "apostila_scraped/images/page_003/img_02.png", "section": "Bolsa de Valores"}
  ],
  "page_9": [
    {"image_id": "pg_009_img_01", "file": "apostila_scraped/images/page_009/img_01.png", "section": "Análise dos Candles"}
  ]
}
```

### PASSO 3: RECONSTRUIR JSON DE CONTEÚDO (30 min)
Ler pdf_texto_completo.txt + image_mapping.json e gerar:

```json
{
  "topics": [
    {
      "title": "MÓDULO BÁSICO 1 - CONHECIMENTOS BÁSICOS",
      "subtopics": [
        {
          "title": "Bolsa de Valores",
          "slides": [
            {
              "page": 4,
              "title": "BM&F - Bolsa de Mercadorias",
              "content": "[texto real do PDF]",
              "images": ["apostila_scraped/images/page_004/img_01.png"]
            },
            {
              "page": 5,
              "title": "B3 - Brasil, Bolsa, Balcão",
              "content": "[texto real]",
              "images": ["apostila_scraped/images/page_005/img_01.png"]
            }
          ]
        }
      ]
    }
  ]
}
```

### PASSO 4: ATUALIZAR HTML/JS (20 min)
Modificar index.html para:
```javascript
// Antes:
document.getElementById('content').innerHTML = '<h2>' + slide.title + '</h2><p>' + slide.content + '</p>';

// Depois:
let html = '<h2>' + slide.title + '</h2>';
html += '<p>' + slide.content + '</p>';
if (slide.images && slide.images.length > 0) {
  slide.images.forEach(img => {
    html += '<img src="' + img + '" alt="' + slide.title + '" style="max-width:100%; margin:20px 0;">';
  });
}
document.getElementById('content').innerHTML = html;
```

### PASSO 5: TESTE + DEPLOY (10 min)
```bash
# Local: http://localhost:8000
# Verificar: imagens carregam? conteúdo correto? navegação funciona?

# GitHub Pages:
git add -A
git commit -m "feat: landing page ilustrada com todas as 877 imagens"
git push origin main
```

---

## ESTRUTURA FINAL ESPERADA

```
C:\PROJETO-IA\TRADE\
├── index.html                           (atualizado com <img>)
├── apostila_scraped/
│   ├── landing-page-data.json           (conteúdo real + refs imagens)
│   ├── image_mapping.json               (novo - page → images)
│   ├── images/                          (novo folder)
│   │   ├── page_004/
│   │   │   ├── img_01.png               (877 imagens extraídas)
│   │   │   └── img_02.png
│   │   ├── page_005/
│   │   └── ...
│   └── pdf_extracted.json               (mantido como backup)
├── style.css                            (pode precisar ajuste para imgs)
└── [outros arquivos]
```

---

## ESTIMATIVAS REALISTAS

| Tarefa | Tempo | Tokens |
|--------|-------|--------|
| Extrair 877 imagens | 45 min | 5K-10K |
| Criar JSON mapping | 15 min | 2K-3K |
| Reconstruir dados | 30 min | 8K-12K |
| Atualizar HTML/JS | 20 min | 3K-5K |
| Teste e deploy | 10 min | 2K-3K |
| **TOTAL** | **120 min (2h)** | **20K-33K tokens** |

---

## CHECKLIST PRÉ-EXECUÇÃO (quando tokens resetarem)

- [ ] Tokens resetados? (verifique contador)
- [ ] PDF original existe? `Apostila Ariane Campolim_2324 (1).pdf`
- [ ] PyPDF2 + Pillow instalados? (`pip install PyPDF2 Pillow`)
- [ ] Pasta `apostila_scraped/images/` criada?
- [ ] GitHub token válido para push?

---

## NOTAS IMPORTANTES

1. **Remover "Ariane"**: Ao processar texto, filtrar referências à autora original
2. **Remover números de página**: Usar regex para limpar `\d+` ao final de linhas
3. **Otimizar imagens**: Considerar WebP + lazy loading se muitas imagens
4. **Teste local ANTES de push**: Confirmar carregamento de imagens antes de GitHub Pages
5. **Backup do pdf_extracted.json**: Manter versão original em caso de erro

---

## APÓS RESET DE TOKENS

**Próximo agente que receber isso:**

1. Leia este arquivo (você está aqui)
2. Execute PASSO 1 (extrair imagens)
3. Execute PASSO 2-5 em sequência
4. Reporte status ao Orion

**Comando para começar:**
```
python extract_images_from_pdf.py
```

Script a ser criado no reset: `C:\PROJETO-IA\TRADE\extract_images_from_pdf.py`

---

**Estado salvo em:** `commit bac566c`  
**Branch:** `main`  
**GitHub:** https://github.com/raimundoafilho/price-action-landing-page  
**Local:** http://localhost:8000

🎯 Quando tokens resetarem, começa OPÇÃO B!
