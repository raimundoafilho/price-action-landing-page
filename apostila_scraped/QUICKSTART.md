# Quickstart — Pipeline de Imagens

Comece em 5 minutos.

## Pré-requisitos

### Windows (PowerShell)

```powershell
# 1. Verificar Python
python --version

# 2. Instalar dependências
pip install pdfplumber pillow
```

### macOS/Linux

```bash
# 1. Verificar Python
python3 --version

# 2. Instalar dependências
pip3 install pdfplumber pillow
```

## Validação Rápida (2 min)

```bash
# Verificar se tudo está pronto
python validate_pipeline.py
```

Deve mostrar:
```
✓ JSON
✓ PDF
✓ Dependencies
✓ Directories
✓ Output
✓ Optimization

✓ Pipeline pronto para execução!
```

Se há erros, instale dependências:
```bash
pip install pdfplumber pillow
```

## Executar Pipeline (3-5 min)

### Opção 1: Automático com Wrapper (Recomendado)

```bash
python run_pipeline.py
```

Saída esperada:
```
============================================================
PIPELINE DE OTIMIZAÇÃO DE IMAGENS
============================================================

Verificando dependências...
  ✓ pdfplumber
  ✓ pillow

Carregando metadata de image-manifest.json
Total de imagens em metadata: 877

============================================================
OTIMIZANDO IMAGENS...
============================================================
Processadas 877/877 imagens

Criando manifest.json...
✓ Manifest salvo em image-manifest.json

============================================================
ESTATÍSTICAS DE OTIMIZAÇÃO
============================================================
totalImages....................... 877
totalWebpMb...................... 12.4
totalPngMb....................... 31.2
estimatedReductionPercent........ 72

============================================================
VALIDAÇÃO
============================================================
WebP files: 877
PNG fallback files: 877
Manifest entries: 877

✓ Pipeline finalizado com sucesso!
```

### Opção 2: Python Direto

```bash
python pipeline_images.py
```

### Opção 3: Node.js

```bash
npm install -g sharp
node pipeline-images.js
```

## Verificar Resultado

```bash
# Contar arquivos gerados
ls images-webp/*.webp | wc -l      # Deve ser 877
ls images-fallback/*.png | wc -l    # Deve ser 877

# Ver manifest
cat image-manifest.json | head -50

# Ver uma imagem específica
ls -lh images-webp/img_001_01.webp
ls -lh images-fallback/img_001_01.png
```

## Estrutura Final

```
apostila_scraped/
├── pdf_extracted.json           # Entrada: metadata bruta
├── image-manifest.json          # Saída: índice (877 imagens)
├── images-webp/                 # Saída: 877 WebP otimizadas
│   ├── img_001_01.webp
│   ├── img_001_02.webp
│   └── ... (875 mais)
├── images-fallback/             # Saída: 877 PNG fallback
│   ├── img_001_01.png
│   ├── img_001_02.png
│   └── ... (875 mais)
└── PIPELINE_README.md           # Documentação completa
```

## Usar em Aplicação Web

```html
<!DOCTYPE html>
<html>
<body>
  <h1>Apostila com Imagens Otimizadas</h1>
  
  <picture>
    <source srcset="images-webp/img_001_01.webp" type="image/webp">
    <img src="images-fallback/img_001_01.png" alt="Imagem 1">
  </picture>
  
  <script type="module">
    import manifest from './image-manifest.json' assert { type: 'json' };
    
    console.log(`Carregadas ${manifest.images.length} imagens`);
    manifest.images.forEach(img => {
      console.log(`${img.id}: ${img.type} (${img.webpSizeKb}KB)`);
    });
  </script>
</body>
</html>
```

## Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'pdfplumber'"

```bash
pip install pdfplumber
```

### Erro: "PDF não encontrado"

Verificar se existe:
```bash
ls "C:/PROJETO-IA/TRADE/Oliver-Velez-Metodo/Apostila Ariane Campolim_2324 (1).pdf"
```

### Erro: "sharp not found"

```bash
npm install -g sharp
```

### Windows: "python não é reconhecido"

Use `python3` ou caminho completo:
```bash
C:\Users\Cliente\AppData\Local\Python\pythoncore-3.14-64\python.exe run_pipeline.py
```

## Próximos Passos

1. **Usar em aplicação**
   - Ver `INTEGRATION_GUIDE.md` para exemplos React/Vue

2. **Customizar limites de tamanho**
   - Editar `RESIZE_LIMITS` em `pipeline_images.py`
   - Re-executar pipeline

3. **Melhorar qualidade**
   - Aumentar `QUALITY_WEBP` para 85+ (mais lento)
   - Ajustar `quality=82` em linha 89

4. **Gerar variantes retina**
   - Implementar `RESIZE_LIMITS` com 1x e 2x

## Tempo Esperado

- Validação: ~10 segundos
- Pipeline (877 imagens): 2-5 minutos
- Total: ~3-6 minutos

Depende de:
- Velocidade do disco
- CPU disponível
- Qualidade WebP (6 = lento mas bom)

## Próxima Execução

Se precisar regenerar imagens (após mudar limites, etc):

```bash
# Limpar saídas antigas
rm -rf images-webp images-fallback image-manifest.json

# Re-executar
python run_pipeline.py
```

## Suporte

Ver `PIPELINE_README.md` para documentação completa.

## Checklist Final

- [ ] Validação passou ✓
- [ ] Pipeline executou com sucesso ✓
- [ ] 877 WebP criadas ✓
- [ ] 877 PNG criadas ✓
- [ ] image-manifest.json válido ✓
- [ ] Imagens testadas em browser ✓
- [ ] Integrado em aplicação ✓

**Pronto! Seu pipeline está operacional.**
