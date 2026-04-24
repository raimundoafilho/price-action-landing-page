# Pipeline de Otimização de Imagens

Automatiza a extração, otimização e indexação de imagens do PDF da apostila.

## Estrutura

```
apostila_scraped/
├── pdf_extracted.json              # Metadata bruta do PDF (877 imagens)
├── pipeline_images.py              # Pipeline Python (recomendado)
├── run_pipeline.py                 # Wrapper com verificação de dependências
├── pipeline-images.js              # Pipeline Node.js (alternativo)
├── image-manifest.json             # Índice final (gerado)
├── images-webp/                    # 877 WebP otimizadas (gerado)
├── images-fallback/                # 877 PNG fallback (gerado)
└── PIPELINE_README.md              # Este arquivo
```

## Requisitos

### Python (Recomendado)
- Python 3.7+
- pdfplumber (extração do PDF)
- Pillow (processamento de imagens)
- setuptools-scm (dependência interna)

```bash
pip install pdfplumber pillow
```

### Node.js (Alternativo)
- Node.js 14+
- sharp (processamento de imagens)

```bash
npm install -g sharp
```

## Uso

### Opção 1: Python (Recomendado)

```bash
# Executar com wrapper (recomendado - instala dependências automaticamente)
python3 run_pipeline.py

# Ou executar diretamente
python3 pipeline_images.py
```

### Opção 2: Node.js

```bash
node pipeline-images.js
```

### Opção 3: PowerShell

```powershell
cd C:\PROJETO-IA\TRADE\apostila_scraped
python run_pipeline.py
```

## Fluxo de Execução

```
1. VERIFICAÇÃO DE DEPENDÊNCIAS
   └─> Instala pdfplumber, Pillow se faltarem

2. CARREGAMENTO DE METADATA
   └─> Lê pdf_extracted.json (877 imagens)
       - Extrai dimensões
       - Detecta tipo (chart, screenshot, icon, default)

3. EXTRAÇÃO DE IMAGENS
   ├─> Tenta extrair do PDF original
   └─> Se falhar, usa heurística de placeholder

4. OTIMIZAÇÃO
   Para cada imagem:
   ├─> Redimensionar conforme tipo:
   │   ├─ Charts: máx 580px
   │   ├─ Screenshots: máx 500px
   │   ├─ Ícones: máx 300px
   │   └─ Default: máx 800px
   ├─> Salvar WebP (qualidade 82%)
   ├─> Salvar PNG (fallback, qualidade 95%)
   └─> Registrar tamanho final

5. CRIAÇÃO DE MANIFEST
   └─> Gera image-manifest.json com:
       - ID único de cada imagem
       - Paths WebP e PNG
       - Dimensões finais
       - Tamanhos em KB
       - Tipo e prioridade

6. VALIDAÇÃO
   ├─> Verifica 877 WebP criadas
   ├─> Verifica 877 PNG criadas
   └─> Valida manifest com 877 entradas
```

## Estrutura do Manifest

```json
{
  "version": "1.0",
  "generatedAt": "2026-04-24T12:00:00.000000",
  "totalImages": 877,
  "images": [
    {
      "id": "img_001_01",
      "page": 1,
      "index": 1,
      "srcWebp": "images-webp/img_001_01.webp",
      "srcPng": "images-fallback/img_001_01.png",
      "type": "chart",
      "finalWidth": 580,
      "finalHeight": 340,
      "webpSizeKb": 45.3,
      "pngSizeKb": 120.5,
      "altText": "Imagem img_001_01 da página 1",
      "priority": "low"
    }
  ]
}
```

## Detecção de Tipo

Baseada em dimensões:

| Tipo | Critério | Limite |
|------|----------|--------|
| **icon** | width < 350 AND height < 350 | 300px max |
| **screenshot** | aspect ratio 0.4-0.7 (tall) | 500px max |
| **chart** | aspect ratio > 1.3 (wide) | 580px max |
| **default** | outros | 800px max |

## Compressão

- **WebP**: Qualidade 82, método 6 (lento mas ótimo)
- **PNG**: Fallback com nível 9 de compressão
- **Redução esperada**: ~75% (de ~56MB para ~14MB)

## Validação

Após execução, verificar:

```bash
# Contar WebP
ls images-webp/*.webp | wc -l  # Deve ser 877

# Contar PNG
ls images-fallback/*.png | wc -l  # Deve ser 877

# Validar manifest
python3 -c "import json; m=json.load(open('image-manifest.json')); print(f'Imagens: {len(m[\"images\"])}')"
```

## Referência em Código

### JavaScript
```javascript
const manifest = require('./image-manifest.json');

manifest.images.forEach(img => {
  // img.srcWebp  -> URL do WebP
  // img.srcPng   -> URL PNG fallback
  // img.type     -> Tipo da imagem
});
```

### Python
```python
import json

with open('image-manifest.json', 'r') as f:
    manifest = json.load(f)

for img in manifest['images']:
    print(f"{img['id']}: {img['srcWebp']}")
```

## Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'pdfplumber'"
```bash
pip install pdfplumber
```

### Erro: "ModuleNotFoundError: No module named 'PIL'"
```bash
pip install pillow
```

### Erro: "PDF não encontrado"
Verificar path do PDF em `pipeline_images.py`:
```python
PDF_PATH = BASE_DIR.parent / "Oliver-Velez-Metodo" / "Apostila Ariane Campolim_2324 (1).pdf"
```

### Erro: "sharp not found" (Node.js)
```bash
npm install -g sharp
# ou
npm install sharp
```

## Performance

- **877 imagens**: ~2-5 minutos (depende do hardware)
- **Memória**: ~500MB pico durante processamento
- **Disco**: ~30MB de saída (WebP + PNG)

## Próximos Passos

1. Integrar manifest em aplicação web
2. Implementar lazy-loading com Intersection Observer
3. Servir WebP com fallback PNG automático
4. Gerar variantes 2x para retina displays
5. Implementar lógica de prioridade (hero images, etc)

## Referências

- [Pdfplumber Docs](https://github.com/jsvine/pdfplumber)
- [Pillow Image Processing](https://pillow.readthedocs.io/)
- [Sharp Image Library](https://sharp.pixelplumbing.com/)
- [WebP Format Spec](https://developers.google.com/speed/webp)
