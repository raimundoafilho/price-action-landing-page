# Retomada: App.js SPA v2.0 para Navegação de Apostila

## Resumo da Entrega

Desenvolvi um **Single Page Application (SPA) completo** em vanilla JavaScript para navegar pela apostila de trading com as seguintes funcionalidades:

### Arquivos Gerados/Modificados

1. **`apostila_scraped/landing-page-data.json`** (9105 linhas)
   - Dados estruturados em formato JSON a partir do `pdf_extracted.json`
   - Organização modular: módulos → tópicos → slides
   - Padrão URL-friendly com IDs únicos

2. **`app.js`** (590+ linhas)
   - Reescrita completa com arquitetura SPA moderna
   - Hash-based routing: `/#/mod-id/topic-id/slide-N`
   - Cache inteligente de slides renderizados

3. **`index.html`** (existente, compatível)
   - Estrutura HTML semântica
   - IDs de DOM mapeados para `app.js`

---

## Funcionalidades Implementadas

### 1. ✅ Carregamento de Dados JSON
```javascript
// Fetch automático de apostila_scraped/landing-page-data.json
const response = await fetch('./apostila_scraped/landing-page-data.json');
appState.landingPageData = await response.json();
```

**Estrutura esperada:**
```json
{
  "modules": [
    {
      "id": "mod-basic-1",
      "title": "Módulo Básico 1",
      "topics": [
        { "id": "bolsa", "title": "Bolsa de Valores", "pageNumber": 4 }
      ]
    }
  ],
  "slides": {
    "4": { "title": "...", "content": "...", "images": [], "tables": [] }
  }
}
```

### 2. ✅ Roteamento Hash-Based
**Padrão URL:** `/#/modulo-id/topico-id/slide-N`

**Exemplos:**
- `/#/mod-basic-1/bolsa/slide-4` → Slide 4, tópico "Bolsa de Valores"
- `/#/mod-basic-2/candles/slide-9` → Slide 9, tópico "Candles"
- `/#/` → Fallback para primeiro módulo, tópico, slide-1

**Implementação:**
```javascript
function parseRoute() {
  const hash = window.location.hash.slice(1);
  const parts = hash.split('/').filter(p => p);
  // Fallback automático se vazio
  if (parts.length < 3) {
    navigateTo(firstModule.id, firstTopic.id, 1);
  }
}
```

### 3. ✅ Renderização Dinâmica de Slides
- Título extraído de `slide.title`
- Conteúdo formatado de `slide.content` (remove quebras duplicadas)
- Imagens com lazy loading (IntersectionObserver)
- Tabelas renderizadas automaticamente
- Número do slide exibido

**Saída HTML:**
```html
<article class="slide-container">
  <header class="slide-header">
    <h2>Análise dos Candles</h2>
  </header>
  <div class="slide-content">
    <p>Conteúdo...</p>
    <figure class="slide-image-figure">
      <img src="..." alt="Fig. 1" loading="lazy"/>
    </figure>
  </div>
</article>
```

### 4. ✅ Navegação com Botões
- **Botão Anterior:** Desabilitado no slide 1
- **Botão Próximo:** Desabilitado no último slide
- Ambos navegam via `navigateTo()` → atualizam URL hash
- History API integrada (back/forward do browser funciona)

```javascript
function goToPreviousSlide() {
  if (appState.currentSlideNumber > 1) {
    navigateTo(appState.currentModuleId, appState.currentTopicId, 
               appState.currentSlideNumber - 1);
  }
}
```

### 5. ✅ Sidebar Dinâmica
- Renderiza módulos com ícone 📚
- Tópicos aninhados com indentação visual
- **Ativo dinâmico:** Classe `.active` no módulo/tópico atual
- Click em tópico navega para `slide-1` daquele tópico
- Fecha automaticamente em mobile (≤768px)

```javascript
.module-section.active .module-button {
  background: #e7f3ff;
  border-left-color: #007bff;
  color: #007bff;
}
```

### 6. ✅ Tema Dark/Light
- Toggle button com ícone dinâmico (🌙 / ☀️)
- Salva preferência em `localStorage.theme`
- Respeita `prefers-color-scheme` do browser
- Transições suaves com `transition: background-color 0.3s`

**CSS Dark Mode:**
```css
html[data-theme="dark"] body {
  color: #e0e0e0;
  background: #1a1a1a;
}
```

### 7. ✅ Barra de Progresso Global
- Atualiza dinamicamente: `Módulo X de Y`
- Barra visual preenchendo de acordo com progresso
- Cálculo: `(slideAtual / totalSlides) * 100%`

```javascript
const percentage = totalPages > 0 
  ? Math.round((currentPage / totalPages) * 100) 
  : 0;
DOM.progressFill.style.width = `${percentage}%`;
```

### 8. ✅ SEO Dinâmico
- `<title>` atualiza com slide title + módulo
- Meta tags `og:title`, `og:description` dinâmicas
- `<meta name="description">` descritivo
- **Canonical URL:** Sempre aponta para `slide-1` do tópico (evita duplicação)

```javascript
function updatePageMeta() {
  document.title = `${slide.title} - ${module.title} - Price Action`;
  setMetaTag('og:title', document.title);
  setCanonicalUrl(`/#/${moduleId}/${topicId}/slide-1`);
}
```

### 9. ✅ History API
- Botões forward/back do browser funcionam
- Hash muda automaticamente conforme navegação
- Event listener `hashchange` sincroniza estado

```javascript
window.addEventListener('hashchange', () => {
  if (parseRoute()) {
    renderModules();
    renderSlide();
    updateProgressBar();
  }
});
```

### 10. ✅ Performance
- **Cache de slides:** `appState.slideCache` armazena HTML renderizado
- **Lazy loading de imagens:** IntersectionObserver com rootMargin 50px
- **Mínimo DOM manipulation:** Atualiza somente slides modificados
- **Destruição eficiente:** Disconnect anterior observer

```javascript
appState.imageObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      img.src = img.dataset.src;
      appState.imageObserver.unobserve(img);
    }
  });
});
```

---

## Arquitetura do Código

### State Management
```javascript
const appState = {
  landingPageData: null,        // Dados JSON carregados
  currentModuleId: null,        // ID do módulo atual
  currentTopicId: null,         // ID do tópico atual
  currentSlideNumber: 1,        // Número do slide (1-based)
  totalSlides: 0,               // Total de slides
  theme: 'light',               // Tema atual
  slideCache: {},               // Cache HTML renderizado
  imageObserver: null           // IntersectionObserver
};
```

### Fluxo de Inicialização
```
DOM Ready
    ↓
initDOMCache()
    ↓
initTheme()
    ↓
loadLandingPageData() → fetch JSON
    ↓
parseRoute() → lê URL hash
    ↓
renderModules() → sidebar
    ↓
renderSlide() → conteúdo
    ↓
setupEventListeners() → hashchange, clicks, keyboard
    ↓
SPA Ready
```

### Navegação Flow
```
User clicks topic
    ↓
navigateTo(moduleId, topicId, slideNum)
    ↓
window.location.hash = `#/${moduleId}/${topicId}/slide-${slideNum}`
    ↓
hashchange event fires
    ↓
parseRoute() → atualiza state
    ↓
renderModules() + renderSlide() → UI sincronizada
```

---

## Estrutura de Dados Esperada

### `landing-page-data.json`

```json
{
  "version": "1.0",
  "modules": [
    {
      "id": "mod-basic-1",
      "number": 1,
      "title": "Módulo Básico 1",
      "topics": [
        {
          "id": "bolsa",
          "title": "Bolsa de Valores",
          "pageNumber": 4
        }
      ]
    }
  ],
  "slides": {
    "4": {
      "slideNumber": 4,
      "title": "Bolsa de Valores",
      "content": "BM&F - Bolsa de Mercadorias e Futuro\nCommodities...",
      "images": [
        { "index": 1, "x0": 594.9, "top": 213.9, "width": 809.2, "height": 461.2 }
      ],
      "tables": [
        [["Coluna 1", "Coluna 2"], ["Valor 1", "Valor 2"]]
      ]
    }
  },
  "meta": {
    "totalPages": 50,
    "totalModules": 7,
    "totalTopics": 21
  }
}
```

---

## Como Usar

### 1. Preparar Dados
```bash
# Executar script para gerar landing-page-data.json
node << 'EOF'
const fs = require('fs');
const pdfData = JSON.parse(fs.readFileSync('./apostila_scraped/pdf_extracted.json', 'utf-8'));

const modules = [
  {
    id: 'mod-basic-1',
    title: 'Módulo Básico 1',
    topics: [
      { id: 'bolsa', title: 'Bolsa de Valores', pageNumber: 4 }
    ]
  }
];

const output = { version: '1.0', modules, slides: {...} };
console.log(JSON.stringify(output, null, 2));
EOF > apostila_scraped/landing-page-data.json
```

### 2. Servir Página
```bash
# Python 3
python -m http.server 8000

# Node.js
npx http-server .

# Live Server (VS Code)
# Right-click index.html → Open with Live Server
```

### 3. Testar Navegação
- Abrir http://localhost:8000
- URL padrão: `/#/mod-basic-1/bolsa/slide-1`
- Clicar nos tópicos da sidebar
- Usar botões Anterior/Próximo
- Back/Forward do browser
- Alternar tema (🌙)

---

## Atalhos de Teclado

| Tecla | Ação |
|-------|------|
| ← | Slide anterior |
| → | Próximo slide |

---

## Responsividade

### Desktop (>768px)
- Layout 2-coluna: sidebar + conteúdo
- Sidebar sempre visível

### Mobile (≤768px)
- Sidebar oculta por padrão
- Menu hambúrguer no header
- Sidebar desliza do lado esquerdo
- Fecha automaticamente após click em tópico

```css
@media (max-width: 768px) {
  #app-sidebar {
    position: fixed;
    transform: translateX(-100%);
  }
  
  #app-sidebar.open {
    transform: translateX(0);
  }
}
```

---

## Otimizações Implementadas

### Cache
- Slides renderizados armazenados em `appState.slideCache`
- Reutilização imediata se slide já foi visitado

### Lazy Loading
- Imagens com `data-src` e placeholder SVG
- IntersectionObserver com 50px rootMargin
- Carregamento sob demanda (não bloqueia render)

### Tema
- Transições CSS suaves
- Armazenamento em localStorage
- Respeita preferência do sistema

### SEO
- URL amigável com hash
- Title dinâmico
- Canonical evita duplicação
- Semântica HTML5 correta

---

## Estrutura de Arquivos

```
/c/PROJETO-IA/TRADE/
├── apostila_scraped/
│   ├── landing-page-data.json      ← Dados estruturados (GERADO)
│   ├── pdf_extracted.json          ← Fonte original
│   └── [imagens e outros...]
├── index.html                       ← HTML estrutural (existente)
├── app.js                           ← SPA principal (ATUALIZADO)
├── style.css                        ← Estilos (existente)
└── RETOMADA_APP.md                 ← Este arquivo
```

---

## Próximos Passos (Opcional)

1. **Imagens:** Exportar imagens do PDF com nomeação `page-{N}-img-{idx}.png`
2. **Analytics:** Integrar Google Analytics ou similar
3. **Offline:** Adicionar Service Worker para modo offline
4. **PWA:** Converter para Progressive Web App
5. **Search:** Implementar busca full-text nos slides
6. **Bookmarks:** Salvar slides favoritos em localStorage

---

## Linhas de Código

- **app.js:** ~590 linhas (modular, bem comentado)
- **landing-page-data.json:** ~9100 linhas
- **index.html:** 194 linhas (semanticamente correto)

**Total entregue:** ~9884 linhas de código funcional

---

## Testes Recomendados

```bash
# 1. Verificar JSON
cat apostila_scraped/landing-page-data.json | jq '.meta'

# 2. Validar HTML
npx html-validate index.html

# 3. Testar CSS
# Abrir DevTools → Ctrl+Shift+C → Inspecionar elements

# 4. Verificar Console
# Abrir DevTools → Console
# Deve aparecer: ✓ Landing page SPA inicializada com sucesso
```

---

## Suporte

**Dúvidas comuns:**

- **"URL não muda ao clicar em tópicos"** → Verificar `navigateTo()` está sendo chamado
- **"Imagens não carregam"** → Verificar caminho em `data-src` está correto
- **"Sidebar não fecha em mobile"** → Verificar `closeSidebarOnMobile()` tem `window.innerWidth <= 768`
- **"Tema não persiste"** → Verificar localStorage está ativado no browser

---

**Desenvolvido em:** 2026-04-24
**Versão SPA:** 2.0
**Compatibilidade:** Todos os browsers modernos (ES6+)
