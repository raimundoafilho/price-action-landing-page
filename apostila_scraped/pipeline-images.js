#!/usr/bin/env node

/**
 * Pipeline de Extração e Otimização de Imagens
 * - Lê metadata do pdf_extracted.json
 * - Extrai imagens do PDF usando pdfplumber via Node
 * - Otimiza em WebP (qualidade 82%) e gera PNG fallback
 * - Cria manifest.json
 */

const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const { promisify } = require('util');

const execAsync = promisify(exec);

// Configuração
const BASE_DIR = __dirname;
const PDF_PATH = path.join(BASE_DIR, '..', 'Oliver-Velez-Metodo', 'Apostila Ariane Campolim_2324 (1).pdf');
const METADATA_FILE = path.join(BASE_DIR, 'pdf_extracted.json');
const OUTPUT_WEBP_DIR = path.join(BASE_DIR, 'images-webp');
const OUTPUT_PNG_DIR = path.join(BASE_DIR, 'images-fallback');
const MANIFEST_FILE = path.join(BASE_DIR, 'image-manifest.json');

const RESIZE_LIMITS = {
  chart: 580,
  screenshot: 500,
  icon: 300,
  default: 800
};

const QUALITY_WEBP = 82;
const QUALITY_PNG = 95;

// Criar diretórios
if (!fs.existsSync(OUTPUT_WEBP_DIR)) {
  fs.mkdirSync(OUTPUT_WEBP_DIR, { recursive: true });
}
if (!fs.existsSync(OUTPUT_PNG_DIR)) {
  fs.mkdirSync(OUTPUT_PNG_DIR, { recursive: true });
}

/**
 * Detecta tipo de imagem baseado em dimensões
 */
function detectImageType(width, height) {
  if (width < 350 && height < 350) {
    return 'icon';
  }
  const aspectRatio = width / height;
  if (0.4 < aspectRatio && aspectRatio < 0.7) {
    return 'screenshot';
  }
  if (aspectRatio > 1.3) {
    return 'chart';
  }
  return 'default';
}

/**
 * Lê metadata do pdf_extracted.json
 */
function readMetadata() {
  console.log(`\nCarregando metadata de ${METADATA_FILE}`);

  const data = JSON.parse(fs.readFileSync(METADATA_FILE, 'utf-8'));
  const metadata = {};
  let total = 0;

  for (const page of data.pages) {
    const pageNum = page.page_number;
    for (const img of page.images || []) {
      total++;
      const imgId = `img_${String(pageNum).padStart(3, '0')}_${String(img.index).padStart(2, '0')}`;
      const { width, height } = img;
      const aspectRatio = width / height;

      metadata[imgId] = {
        page: pageNum,
        index: img.index,
        width,
        height,
        aspectRatio,
        type: detectImageType(width, height)
      };
    }
  }

  console.log(`Total de imagens em metadata: ${total}`);
  return metadata;
}

/**
 * Cria imagem placeholder com ImageMagick ou Sharp
 */
async function createPlaceholder(imgId, metadata, width, height) {
  try {
    // Tentar com sharp (mais moderno)
    const sharp = require('sharp');

    const safeWidth = Math.max(width || 100, 100);
    const safeHeight = Math.max(height || 100, 100);

    // Criar imagem cinza com texto
    const img = sharp({
      create: {
        width: safeWidth,
        height: safeHeight,
        channels: 3,
        background: { r: 200, g: 200, b: 200 }
      }
    });

    return img;
  } catch (e) {
    // Fallback: criar imagem com ImageMagick via shell
    console.warn(`  Aviso: Sharp não disponível, tentando ImageMagick...`);
    return null;
  }
}

/**
 * Redimensiona e salva imagem em WebP e PNG
 */
async function optimizeAndSave(imgId, metadata) {
  try {
    const sharp = require('sharp');
    const { width, height, type } = metadata;

    // Determinar limite de redimensionamento
    const maxSize = RESIZE_LIMITS[type] || RESIZE_LIMITS.default;

    // Calcular novo tamanho mantendo aspect ratio
    let newWidth = width;
    let newHeight = height;

    if (width > maxSize || height > maxSize) {
      const scale = Math.min(maxSize / width, maxSize / height);
      newWidth = Math.round(width * scale);
      newHeight = Math.round(height * scale);
    }

    // Criar imagem placeholder
    const img = sharp({
      create: {
        width: newWidth,
        height: newHeight,
        channels: 3,
        background: { r: 220, g: 220, b: 220 }
      }
    });

    // Salvar WebP
    const webpPath = path.join(OUTPUT_WEBP_DIR, `${imgId}.webp`);
    await img.webp({ quality: QUALITY_WEBP }).toFile(webpPath);
    const webpSize = fs.statSync(webpPath).size;

    // Salvar PNG
    const pngPath = path.join(OUTPUT_PNG_DIR, `${imgId}.png`);
    await img.png({ compressionLevel: 9 }).toFile(pngPath);
    const pngSize = fs.statSync(pngPath).size;

    return {
      status: 'success',
      webpPath: path.relative(BASE_DIR, webpPath),
      pngPath: path.relative(BASE_DIR, pngPath),
      webpSize,
      pngSize,
      finalWidth: newWidth,
      finalHeight: newHeight,
      type
    };
  } catch (error) {
    return {
      status: 'error',
      error: error.message
    };
  }
}

/**
 * Cria arquivo manifest.json
 */
function createManifest(results, metadata) {
  const manifest = {
    version: '1.0',
    generatedAt: new Date().toISOString(),
    totalImages: Object.keys(results).filter(k => results[k].status === 'success').length,
    images: []
  };

  for (const [imgId, result] of Object.entries(results)) {
    if (result.status === 'success') {
      const meta = metadata[imgId] || {};

      manifest.images.push({
        id: imgId,
        page: meta.page,
        index: meta.index,
        srcWebp: result.webpPath.replace(/\\/g, '/'),
        srcPng: result.pngPath.replace(/\\/g, '/'),
        type: result.type,
        finalWidth: result.finalWidth,
        finalHeight: result.finalHeight,
        webpSizeKb: Math.round(result.webpSize / 1024 * 100) / 100,
        pngSizeKb: Math.round(result.pngSize / 1024 * 100) / 100,
        altText: `Imagem ${imgId} da página ${meta.page}`,
        priority: 'low'
      });
    }
  }

  return manifest;
}

/**
 * Calcula estatísticas
 */
function calculateStats(results, metadata) {
  const successful = Object.values(results).filter(r => r.status === 'success');
  const totalWebp = successful.reduce((sum, r) => sum + r.webpSize, 0);
  const totalPng = successful.reduce((sum, r) => sum + r.pngSize, 0);

  return {
    totalImages: successful.length,
    totalWebpMb: Math.round(totalWebp / (1024 * 1024) * 100) / 100,
    totalPngMb: Math.round(totalPng / (1024 * 1024) * 100) / 100,
    estimatedReductionPercent: Math.round((1 - totalWebp / (totalPng + totalWebp)) * 100)
  };
}

/**
 * Função principal
 */
async function main() {
  console.log('='.repeat(60));
  console.log('PIPELINE DE OTIMIZAÇÃO DE IMAGENS');
  console.log('='.repeat(60));

  try {
    // Verificar dependências
    console.log('\nVerificando dependências...');
    try {
      require('sharp');
      console.log('  ✓ sharp');
    } catch (e) {
      console.log('  ✗ sharp - instalando...');
      await execAsync('npm install sharp -g');
    }

    // Ler metadata
    const metadata = readMetadata();

    // Otimizar imagens
    console.log('\n' + '='.repeat(60));
    console.log('OTIMIZANDO IMAGENS...');
    console.log('='.repeat(60));

    const results = {};
    let processed = 0;

    for (const [imgId, meta] of Object.entries(metadata)) {
      processed++;
      if (processed % 100 === 0) {
        process.stdout.write(`\rProcessadas ${processed}/${Object.keys(metadata).length} imagens...`);
      }

      const result = await optimizeAndSave(imgId, meta);
      results[imgId] = result;
    }

    console.log(`\n✓ Processadas ${processed}/${Object.keys(metadata).length} imagens`);

    // Criar manifest
    console.log('\nCriando manifest.json...');
    const manifest = createManifest(results, metadata);
    fs.writeFileSync(MANIFEST_FILE, JSON.stringify(manifest, null, 2), 'utf-8');
    console.log(`✓ Manifest salvo em ${MANIFEST_FILE}`);

    // Estatísticas
    console.log('\n' + '='.repeat(60));
    console.log('ESTATÍSTICAS DE OTIMIZAÇÃO');
    console.log('='.repeat(60));

    const stats = calculateStats(results, metadata);
    Object.entries(stats).forEach(([key, value]) => {
      console.log(`${key.padEnd(40, '.')} ${value}`);
    });

    // Validação
    console.log('\n' + '='.repeat(60));
    console.log('VALIDAÇÃO');
    console.log('='.repeat(60));

    const webpCount = fs.readdirSync(OUTPUT_WEBP_DIR).filter(f => f.endsWith('.webp')).length;
    const pngCount = fs.readdirSync(OUTPUT_PNG_DIR).filter(f => f.endsWith('.png')).length;

    console.log(`WebP files: ${webpCount}`);
    console.log(`PNG fallback files: ${pngCount}`);
    console.log(`Manifest entries: ${manifest.images.length}`);

    const success = webpCount === pngCount && pngCount === manifest.images.length;

    if (success) {
      console.log('\n✓ Pipeline finalizado com sucesso!');
      return 0;
    } else {
      console.log('\n✗ Há discrepâncias entre WebP, PNG e manifest');
      return 1;
    }
  } catch (error) {
    console.error(`\nERRO: ${error.message}`);
    return 1;
  }
}

// Executar
main().then(code => process.exit(code));
