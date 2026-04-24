# Guia de Integração — Image Manifest

Como usar o `image-manifest.json` em sua aplicação web.

## Resumo Rápido

```javascript
// 1. Carregar manifest
const manifest = require('./image-manifest.json');

// 2. Para cada imagem, usar WebP com fallback PNG
manifest.images.forEach(img => {
  console.log(img.srcWebp);   // "images-webp/img_001_01.webp"
  console.log(img.srcPng);    // "images-fallback/img_001_01.png"
  console.log(img.type);      // "chart", "screenshot", etc
});

// 3. No HTML, usar <picture> para fallback automático
```

## Padrão HTML `<picture>`

```html
<picture>
  <source srcset="/images-webp/img_001_01.webp" type="image/webp">
  <img src="/images-fallback/img_001_01.png" alt="Imagem da página 1">
</picture>
```

## Integração JavaScript

### Componente React

```jsx
import manifest from './image-manifest.json';

function ImageViewer({ imageId }) {
  const img = manifest.images.find(i => i.id === imageId);

  if (!img) return null;

  return (
    <picture>
      <source srcSet={img.srcWebp} type="image/webp" />
      <img
        src={img.srcPng}
        alt={img.altText}
        width={img.finalWidth}
        height={img.finalHeight}
        loading="lazy"
      />
    </picture>
  );
}
```

### Vue 3

```vue
<template>
  <picture v-if="image">
    <source :srcset="image.srcWebp" type="image/webp" />
    <img
      :src="image.srcPng"
      :alt="image.altText"
      :width="image.finalWidth"
      :height="image.finalHeight"
      loading="lazy"
    />
  </picture>
</template>

<script setup>
import { computed } from 'vue';
import manifest from './image-manifest.json';

const props = defineProps({
  imageId: String
});

const image = computed(() =>
  manifest.images.find(i => i.id === props.imageId)
);
</script>
```

### Vanilla JavaScript

```javascript
import manifest from './image-manifest.json';

function renderImage(containerId, imageId) {
  const img = manifest.images.find(i => i.id === imageId);
  
  if (!img) {
    console.error(`Imagem ${imageId} não encontrada`);
    return;
  }

  const container = document.getElementById(containerId);
  
  const picture = document.createElement('picture');
  
  const source = document.createElement('source');
  source.srcSet = img.srcWebp;
  source.type = 'image/webp';
  picture.appendChild(source);
  
  const imgEl = document.createElement('img');
  imgEl.src = img.srcPng;
  imgEl.alt = img.altText;
  imgEl.width = img.finalWidth;
  imgEl.height = img.finalHeight;
  imgEl.loading = 'lazy';
  picture.appendChild(imgEl);
  
  container.appendChild(picture);
}

// Uso
renderImage('image-container', 'img_001_01');
```

## Lazy Loading com Intersection Observer

```javascript
import manifest from './image-manifest.json';

function setupLazyLoading() {
  const imageElements = document.querySelectorAll('[data-image-id]');
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const imgId = entry.target.dataset.imageId;
        const img = manifest.images.find(i => i.id === imgId);
        
        if (img) {
          // Atualizar sources
          entry.target.querySelector('source').srcSet = img.srcWebp;
          entry.target.querySelector('img').src = img.srcPng;
          observer.unobserve(entry.target);
        }
      }
    });
  });
  
  imageElements.forEach(el => observer.observe(el));
}
```

HTML correspondente:
```html
<picture data-image-id="img_001_01">
  <source srcset="data:image/webp,..." type="image/webp">
  <img src="data:image/png,..." alt="..." />
</picture>
```

## Servir com HTTP

### Express.js

```javascript
const express = require('express');
const manifest = require('./image-manifest.json');

const app = express();

// Servir arquivos estáticos
app.use('/images-webp', express.static('images-webp'));
app.use('/images-fallback', express.static('images-fallback'));

// API para obter metadados
app.get('/api/images/:id', (req, res) => {
  const img = manifest.images.find(i => i.id === req.params.id);
  
  if (!img) {
    return res.status(404).json({ error: 'Image not found' });
  }
  
  res.json(img);
});

// API para imagens por página
app.get('/api/page/:page', (req, res) => {
  const pageImages = manifest.images.filter(
    i => i.page === parseInt(req.params.page)
  );
  
  res.json(pageImages);
});

app.listen(3000);
```

### Next.js

```javascript
// pages/api/images/[id].js
import manifest from '../../../image-manifest.json';

export default function handler(req, res) {
  const { id } = req.query;
  const img = manifest.images.find(i => i.id === id);
  
  if (!img) {
    return res.status(404).json({ error: 'Not found' });
  }
  
  res.status(200).json(img);
}
```

Uso no componente:
```jsx
// pages/images/[id].jsx
import manifest from '../../image-manifest.json';

export default function ImagePage({ image }) {
  return (
    <picture>
      <source srcSet={image.srcWebp} type="image/webp" />
      <img src={image.srcPng} alt={image.altText} />
    </picture>
  );
}

export async function getStaticPaths() {
  return {
    paths: manifest.images.map(img => ({
      params: { id: img.id }
    })),
    fallback: false
  };
}

export async function getStaticProps({ params }) {
  const image = manifest.images.find(i => i.id === params.id);
  return { props: { image } };
}
```

## Otimizações Avançadas

### Responsive Images

```html
<picture>
  <source 
    media="(min-width: 1024px)"
    srcset="
      /images-webp/img_001_01.webp 1x,
      /images-webp/img_001_01-2x.webp 2x
    "
    type="image/webp"
  >
  <source 
    media="(min-width: 1024px)"
    srcset="
      /images-fallback/img_001_01.png 1x,
      /images-fallback/img_001_01-2x.png 2x
    "
  >
  <img src="/images-fallback/img_001_01.png" alt="..." />
</picture>
```

### Blur-Up (Progressive Loading)

```html
<div class="image-wrapper">
  <img
    class="blur-up"
    src="data:image/png;base64,iVBORw0KGgo..."
    alt="..."
  />
  <picture class="full-image">
    <source srcset="/images-webp/img_001_01.webp" type="image/webp" />
    <img src="/images-fallback/img_001_01.png" alt="..." />
  </picture>
</div>
```

CSS:
```css
.image-wrapper {
  position: relative;
  overflow: hidden;
}

.blur-up {
  position: absolute;
  inset: 0;
  filter: blur(20px);
  opacity: 1;
  transition: opacity 0.3s;
}

.full-image {
  position: relative;
  z-index: 1;
}

.full-image img {
  opacity: 0;
  transition: opacity 0.3s;
}

.full-image img.loaded {
  opacity: 1;
}
```

### Carregamento com Srcset

```html
<picture>
  <source
    srcset="
      /images-webp/img_001_01-small.webp 400w,
      /images-webp/img_001_01-medium.webp 800w,
      /images-webp/img_001_01.webp 1200w
    "
    type="image/webp"
    sizes="(max-width: 600px) 100vw, (max-width: 1200px) 50vw, 33vw"
  />
  <img
    src="/images-fallback/img_001_01.png"
    alt="..."
    loading="lazy"
  />
</picture>
```

## Performance Monitoring

```javascript
// Rastrear carregamento de imagens
function trackImagePerformance() {
  const observer = new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      if (entry.name.includes('images-')) {
        console.log({
          url: entry.name,
          duration: entry.duration,
          size: entry.transferSize,
          type: entry.name.includes('.webp') ? 'webp' : 'png'
        });
      }
    }
  });

  observer.observe({ entryTypes: ['resource'] });
}

trackImagePerformance();
```

## Fallback para Browsers Antigos

```html
<picture>
  <source srcset="/images-webp/img_001_01.webp" type="image/webp">
  <source srcset="/images-fallback/img_001_01.png" type="image/png">
  <!-- Fallback para IE -->
  <img src="/images-fallback/img_001_01.png" alt="...">
</picture>
```

## Suporte CMS/Headless

### GraphQL Query

```graphql
{
  image(id: "img_001_01") {
    id
    page
    type
    srcWebp
    srcPng
    finalWidth
    finalHeight
    altText
  }
}
```

### REST API

```
GET /api/images/img_001_01
GET /api/pages/1/images
GET /api/images?type=chart
GET /api/images?priority=high
```

## Validação de Browser

```javascript
// Detectar suporte WebP
function supportsWebp() {
  const canvas = document.createElement('canvas');
  return canvas.toDataURL('image/webp') !== canvas.toDataURL('image/png');
}

// Usar ao renderizar
const srcset = supportsWebp()
  ? manifest.images[0].srcWebp
  : manifest.images[0].srcPng;
```

## Checklist de Integração

- [ ] Copiar `image-manifest.json` para sua aplicação
- [ ] Servir diretórios `images-webp/` e `images-fallback/` estaticamente
- [ ] Implementar componente de imagem com `<picture>`
- [ ] Configurar lazy loading
- [ ] Testar em múltiplos browsers
- [ ] Validar compressão e tamanhos
- [ ] Implementar error handling
- [ ] Monitorar performance
- [ ] Documentar paths relativos

## Troubleshooting

### Imagens não carregam
- Verificar paths em manifest.json
- Validar estrutura de diretórios
- Confirmar permissões de arquivo

### WebP não exibido
- Verificar suporte do browser
- Validar mime type `image/webp`
- Testar fallback PNG

### Performance lenta
- Implementar lazy loading
- Verificar tamanhos WebP
- Considerar CDN
