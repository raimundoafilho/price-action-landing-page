#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Carregar JSON
const jsonPath = path.join(__dirname, 'pdf_extracted.json');
const data = JSON.parse(fs.readFileSync(jsonPath, 'utf-8'));

const pages = data.pages || [];
console.log(`Total de páginas: ${pages.length}`);

// Coleta de dados
const imagesPerPage = [];
const allImages = [];
const widths = [];
const heights = [];
const xPositions = [];
const yPositions = [];
const pageImageData = {};

pages.forEach(page => {
  const pageNum = page.page_number;
  const images = page.images || [];
  imagesPerPage.push(images.length);
  pageImageData[pageNum] = images;

  images.forEach(img => {
    allImages.push({ page: pageNum, img });
    const w = img.width || 0;
    const h = img.height || 0;
    const x = img.x0 || 0;
    const y = img.top || 0;

    if (w > 0) widths.push(w);
    if (h > 0) heights.push(h);
    if (x >= 0) xPositions.push(x);
    if (y >= 0) yPositions.push(y);
  });
});

function stats(arr) {
  if (arr.length === 0) return { min: 0, max: 0, mean: 0, median: 0 };
  arr.sort((a, b) => a - b);
  const min = arr[0];
  const max = arr[arr.length - 1];
  const mean = arr.reduce((a, b) => a + b, 0) / arr.length;
  const median = arr.length % 2 === 0
    ? (arr[arr.length / 2 - 1] + arr[arr.length / 2]) / 2
    : arr[Math.floor(arr.length / 2)];
  return { min, max, mean, median };
}

// Estatísticas gerais
const totalImgs = allImages.length;
const totalPages = pages.length;
const pagesWithImages = imagesPerPage.filter(x => x > 0).length;

console.log('\n=== ESTATÍSTICAS GERAIS ===');
console.log(`Total de imagens: ${totalImgs}`);
console.log(`Páginas com imagens: ${pagesWithImages}/${totalPages}`);
console.log(`Páginas sem imagens: ${totalPages - pagesWithImages}`);

const imgStats = stats(imagesPerPage.filter(x => x > 0));
console.log(`\nImagens por página (apenas com imagens):`);
console.log(`  Min: ${imagesPerPage.length > 0 ? Math.min(...imagesPerPage) : 0}`);
console.log(`  Max: ${imagesPerPage.length > 0 ? Math.max(...imagesPerPage) : 0}`);
console.log(`  Média: ${(imagesPerPage.reduce((a, b) => a + b, 0) / imagesPerPage.length).toFixed(2)}`);

// Distribuição
const dist0 = imagesPerPage.filter(x => x === 0).length;
const dist1_2 = imagesPerPage.filter(x => x >= 1 && x <= 2).length;
const dist3_5 = imagesPerPage.filter(x => x >= 3 && x <= 5).length;
const dist6plus = imagesPerPage.filter(x => x >= 6).length;

console.log('\n=== DISTRIBUIÇÃO POR PÁGINA ===');
console.log(`  0 imagens: ${dist0} (${(100 * dist0 / totalPages).toFixed(1)}%)`);
console.log(`  1-2 imagens: ${dist1_2} (${(100 * dist1_2 / totalPages).toFixed(1)}%)`);
console.log(`  3-5 imagens: ${dist3_5} (${(100 * dist3_5 / totalPages).toFixed(1)}%)`);
console.log(`  6+ imagens: ${dist6plus} (${(100 * dist6plus / totalPages).toFixed(1)}%)`);

// Dimensões
const wStats = stats(widths);
const hStats = stats(heights);

console.log('\n=== DIMENSÕES ===');
console.log(`Width: min=${wStats.min.toFixed(0)}, max=${wStats.max.toFixed(0)}, média=${wStats.mean.toFixed(0)}, mediana=${wStats.median.toFixed(0)}`);
console.log(`Height: min=${hStats.min.toFixed(0)}, max=${hStats.max.toFixed(0)}, média=${hStats.mean.toFixed(0)}, mediana=${hStats.median.toFixed(0)}`);

// Posições
const xStats = stats(xPositions);
const yStats = stats(yPositions);

console.log('\n=== POSIÇÕES ===');
console.log(`X (x0): min=${xStats.min.toFixed(0)}, max=${xStats.max.toFixed(0)}, média=${xStats.mean.toFixed(0)}`);
console.log(`Y (top): min=${yStats.min.toFixed(0)}, max=${yStats.max.toFixed(0)}, média=${yStats.mean.toFixed(0)}`);

// Categorização por tamanho
const large = allImages.filter(x => (x.img.width || 0) > 400).length;
const medium = allImages.filter(x => (x.img.width || 0) >= 200 && (x.img.width || 0) <= 400).length;
const small = allImages.filter(x => (x.img.width || 0) < 200 || (x.img.width || 0) === 0).length;

console.log('\n=== CATEGORIZAÇÃO POR TAMANHO ===');
console.log(`Grandes (>400): ${large} (${(100 * large / totalImgs).toFixed(1)}%)`);
console.log(`Médias (200-400): ${medium} (${(100 * medium / totalImgs).toFixed(1)}%)`);
console.log(`Pequenas (<200 ou indefinido): ${small} (${(100 * small / totalImgs).toFixed(1)}%)`);

// Detalhes de distribuição por largura
const buckets = {
  '0-100': allImages.filter(x => (x.img.width || 0) < 100).length,
  '100-200': allImages.filter(x => (x.img.width || 0) >= 100 && (x.img.width || 0) < 200).length,
  '200-400': allImages.filter(x => (x.img.width || 0) >= 200 && (x.img.width || 0) <= 400).length,
  '400-600': allImages.filter(x => (x.img.width || 0) > 400 && (x.img.width || 0) <= 600).length,
  '600-800': allImages.filter(x => (x.img.width || 0) > 600 && (x.img.width || 0) <= 800).length,
  '800+': allImages.filter(x => (x.img.width || 0) > 800).length,
};

console.log('\n=== DISTRIBUIÇÃO DETALHADA DE LARGURA ===');
Object.entries(buckets).forEach(([range, count]) => {
  console.log(`  ${range}px: ${count} (${(100 * count / totalImgs).toFixed(1)}%)`);
});

// Páginas com alta concentração
const highConc = [];
imagesPerPage.forEach((count, idx) => {
  if (count > 5) {
    highConc.push({ page: idx + 1, count });
  }
});

console.log('\n=== PÁGINAS COM ALTA CONCENTRAÇÃO (>5 imagens) ===');
console.log(`Total: ${highConc.length} páginas`);
highConc.sort((a, b) => b.count - a.count).slice(0, 15).forEach(item => {
  console.log(`  Página ${item.page}: ${item.count} imagens`);
});

// Páginas críticas (primeiras de cada módulo, com grandes imagens)
console.log('\n=== PÁGINAS CRÍTICAS (Primeiras/Principais) ===');
const criticalPages = [];
const modulePages = new Set();
pages.forEach((page, idx) => {
  const text = page.text || '';
  if (text.includes('Módulo') || text.includes('CONHECIMENTOS') || text.includes('INTRODUÇÃO')) {
    modulePages.add(page.page_number);
  }
});

pages.forEach(page => {
  const images = page.images || [];
  const hasLargeImg = images.some(img => (img.width || 0) > 400);
  if (modulePages.has(page.page_number) || hasLargeImg) {
    criticalPages.push({
      page: page.page_number,
      images: images.length,
      hasLargeImg,
      isModule: modulePages.has(page.page_number)
    });
  }
});

criticalPages.slice(0, 20).forEach(item => {
  console.log(`  Página ${item.page}: ${item.images} imagens${item.isModule ? ' (MÓDULO)' : ''}${item.hasLargeImg ? ' (GRANDE)' : ''}`);
});

// Amostra de imagem
console.log('\n=== AMOSTRA DE IMAGEM ===');
if (allImages.length > 0) {
  const sample = allImages[0];
  console.log(`Primeira imagem (página ${sample.page}):`);
  console.log(JSON.stringify(sample.img, null, 2));
}

// Salvar resultado em arquivo
const output = {
  summary: {
    totalPages,
    totalImages: totalImgs,
    pagesWithImages,
    pagesWithoutImages: totalPages - pagesWithImages,
  },
  distribution: {
    zero: { count: dist0, percentage: (100 * dist0 / totalPages).toFixed(1) },
    one_two: { count: dist1_2, percentage: (100 * dist1_2 / totalPages).toFixed(1) },
    three_five: { count: dist3_5, percentage: (100 * dist3_5 / totalPages).toFixed(1) },
    six_plus: { count: dist6plus, percentage: (100 * dist6plus / totalPages).toFixed(1) },
  },
  imagesPerPage: {
    min: imagesPerPage.length > 0 ? Math.min(...imagesPerPage) : 0,
    max: imagesPerPage.length > 0 ? Math.max(...imagesPerPage) : 0,
    average: (imagesPerPage.reduce((a, b) => a + b, 0) / imagesPerPage.length).toFixed(2),
  },
  dimensions: {
    width: {
      min: wStats.min.toFixed(0),
      max: wStats.max.toFixed(0),
      average: wStats.mean.toFixed(0),
      median: wStats.median.toFixed(0),
    },
    height: {
      min: hStats.min.toFixed(0),
      max: hStats.max.toFixed(0),
      average: hStats.mean.toFixed(0),
      median: hStats.median.toFixed(0),
    },
  },
  categorization: {
    large: { count: large, percentage: (100 * large / totalImgs).toFixed(1) },
    medium: { count: medium, percentage: (100 * medium / totalImgs).toFixed(1) },
    small: { count: small, percentage: (100 * small / totalImgs).toFixed(1) },
  },
  widthBuckets: buckets,
  highConcentrationPages: highConc.sort((a, b) => b.count - a.count),
};

fs.writeFileSync(
  path.join(__dirname, 'image_analysis.json'),
  JSON.stringify(output, null, 2),
  'utf-8'
);

console.log('\n✓ Análise salva em: image_analysis.json');
