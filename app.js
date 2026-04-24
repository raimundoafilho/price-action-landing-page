/**
 * ============================================================================
 * LANDING PAGE PRICE ACTION — APPLICATION JAVASCRIPT (SPA v2.0)
 *
 * Responsável por:
 * - Carregar JSON de dados (landing-page-data.json)
 * - Renderizar slides e navegação com hash-based routing
 * - Gerenciar tema dark/light com localStorage
 * - Sincronizar sidebar, conteúdo e URL
 * - Controlar progresso global
 * - Lazy loading de imagens com IntersectionObserver
 * - SEO dinâmico (title, meta tags, canonical)
 * - History API para navegação back/forward do browser
 * - Cache de slides renderizados
 *
 * Padrão URL: /#/modulo-id/topico-id/slide-N
 * Exemplo: /#/mod-basic-1/bolsa/slide-4
 *
 * Versão: 2.0
 * Data: 2026-04-24
 * ============================================================================
 */

'use strict';

/**
 * ============================================================================
 * AUTENTICAÇÃO COM SENHA
 * ============================================================================
 */
const CORRECT_PASSWORD = 'AndreTrader';

function submitPassword() {
  const input = document.getElementById('passwordInput');
  const pwd = input.value.trim();

  if (pwd === CORRECT_PASSWORD) {
    // Senha correta — salvar em sessionStorage
    sessionStorage.setItem('authenticated', 'true');
    showLandingPage();
    input.value = '';
  } else {
    // Senha incorreta — exibir erro
    const errorElement = document.getElementById('loginError');
    errorElement.textContent = '❌ Senha incorreta. Tente novamente.';
    input.value = '';
    input.focus();
  }
}

function logout() {
  // Limpar autenticação e recarregar página
  sessionStorage.removeItem('authenticated');
  location.reload();
}

function showLandingPage() {
  // Ocultar login screen e mostrar landing page
  const loginScreen = document.getElementById('login-screen');
  const slideContainer = document.getElementById('slideContainer');

  if (loginScreen) loginScreen.style.display = 'none';
  if (slideContainer) slideContainer.style.display = 'block';

  // Inicializar a landing page
  initialize();
}

/**
 * Verificar autenticação ao carregar página
 */
function checkAuthentication() {
  const isAuthenticated = sessionStorage.getItem('authenticated') === 'true';
  const loginScreen = document.getElementById('login-screen');
  const slideContainer = document.getElementById('slideContainer');

  if (isAuthenticated) {
    // Usuário autenticado — mostrar landing page
    if (loginScreen) loginScreen.style.display = 'none';
    if (slideContainer) slideContainer.style.display = 'block';
    showLandingPage();
  } else {
    // Usuário NÃO autenticado — mostrar login screen
    if (loginScreen) loginScreen.style.display = 'flex';
    if (slideContainer) slideContainer.style.display = 'none';

    // Focar no input de senha
    const passwordInput = document.getElementById('passwordInput');
    if (passwordInput) {
      passwordInput.focus();

      // Enter key para submeter
      passwordInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
          submitPassword();
        }
      });
    }
  }
}

/**
 * APPLICATION STATE
 */
const appState = {
  landingPageData: null,
  currentModuleId: null,
  currentTopicId: null,
  currentSlideNumber: 1,
  totalSlides: 0,
  theme: localStorage.getItem('theme') || 'light',
  isLoading: false,
  slideCache: {}, // Cache de slides renderizados
  imageObserver: null // IntersectionObserver para lazy loading
};

/**
 * DOM ELEMENTS CACHE
 */
const DOM = {
  themeToggle: null,
  sidebarToggle: null,
  sidebar: null,
  sidebarNav: null,
  modulesList: null,
  slideContainer: null,
  slideLoading: null,
  slideContent: null,
  slideError: null,
  prevButton: null,
  nextButton: null,
  slideIndicator: null,
  topicIndicator: null,
  progressText: null,
  progressFill: null,
  versionInfo: null
};

/**
 * Inicializar DOM cache
 */
function initDOMCache() {
  DOM.themeToggle = document.getElementById('themeToggle');
  DOM.sidebarToggle = document.getElementById('sidebarToggle');
  DOM.sidebar = document.querySelector('.sidebar');
  DOM.sidebarNav = document.getElementById('sidebarNav');
  DOM.modulesList = document.getElementById('modulesList');
  DOM.slideContainer = document.getElementById('slideContainer');
  DOM.slideLoading = document.getElementById('slideLoading');
  DOM.slideContent = document.getElementById('slideContent');
  DOM.slideError = document.getElementById('slideError');
  DOM.prevButton = document.getElementById('prevButton');
  DOM.nextButton = document.getElementById('nextButton');
  DOM.slideIndicator = document.getElementById('slideIndicator');
  DOM.topicIndicator = document.getElementById('topicIndicator');
  DOM.progressText = document.getElementById('progressText');
  DOM.progressFill = document.getElementById('progressFill');
  DOM.versionInfo = document.getElementById('versionInfo');

  // Gerar header dinâmico se não existir
  const headerElement = document.querySelector('.header') || document.querySelector('#app-header');
  if (!headerElement) {
    const tempHeader = document.createElement('header');
    tempHeader.className = 'header';
    tempHeader.role = 'banner';
    document.body.insertBefore(tempHeader, document.body.firstChild);
  }
}

/**
 * CARREGAMENTO DE DADOS COM CACHE
 */
async function loadLandingPageData() {
  appState.isLoading = true;

  try {
    const response = await fetch('./apostila_scraped/landing-page-data.json');
    if (!response.ok) throw new Error(`HTTP ${response.status}`);

    appState.landingPageData = await response.json();
    window.landingPageData = appState.landingPageData;

    calculateTotalSlides();

    console.log('Landing page data carregado com sucesso');
    console.log(`Modulos: ${appState.landingPageData.modules?.length || 0}`);
    console.log(`Total de slides: ${appState.totalSlides}`);

    appState.isLoading = false;
    return true;
  } catch (error) {
    console.error('Erro ao carregar dados:', error.message);
    showError(`Erro ao carregar: ${error.message}`);
    appState.isLoading = false;
    return false;
  }
}

/**
 * Calcular total de slides (páginas PDF)
 */
function calculateTotalSlides() {
  if (!appState.landingPageData?.slides) {
    appState.totalSlides = 0;
    return;
  }
  appState.totalSlides = Object.keys(appState.landingPageData.slides).length;
}

/**
 * ROTEAMENTO HASH-BASED
 * Processa URL: /#/mod-id/topic-id/slide-N
 */
function parseRoute() {
  const hash = window.location.hash.slice(1);
  const parts = hash.split('/').filter(p => p);

  if (parts.length < 3) {
    // Fallback: primeiro módulo, primeiro tópico, slide 1
    const firstModule = appState.landingPageData?.modules?.[0];
    if (firstModule) {
      const firstTopic = firstModule.topics?.[0];
      if (firstTopic) {
        navigateTo(firstModule.id, firstTopic.id, 1);
        return;
      }
    }
    return false;
  }

  const [moduleId, topicId, slideStr] = parts;
  const slideNum = slideStr?.includes('slide-')
    ? parseInt(slideStr.replace('slide-', ''))
    : 1;

  appState.currentModuleId = moduleId;
  appState.currentTopicId = topicId;
  appState.currentSlideNumber = Math.max(1, slideNum);

  return true;
}

/**
 * Navega para módulo/tópico/slide específico
 */
function navigateTo(moduleId, topicId, slideNum = 1) {
  const newHash = `#/${moduleId}/${topicId}/slide-${slideNum}`;
  window.location.hash = newHash;
}

/**
 * RENDERIZAÇÃO DE MÓDULOS (SIDEBAR)
 */
function renderModules() {
  if (!appState.landingPageData?.modules || appState.landingPageData.modules.length === 0) {
    DOM.modulesList.innerHTML = '<li class="module-item error"><span>Nenhum módulo disponível</span></li>';
    return;
  }

  const html = appState.landingPageData.modules
    .map((module) => {
      const isActive = module.id === appState.currentModuleId;
      const topicsHtml = (module.topics || [])
        .map((topic) => {
          const topicActive = isActive && topic.id === appState.currentTopicId;
          return `
            <li class="topic-item ${topicActive ? 'active' : ''}">
              <button
                class="topic-button"
                data-module-id="${module.id}"
                data-topic-id="${topic.id}"
                data-page="${topic.pageNumber}"
                aria-label="Tópico: ${topic.title || 'Sem título'}"
              >
                ${topic.title || 'Sem título'}
              </button>
            </li>
          `;
        })
        .join('');

      return `
        <li class="module-item ${isActive ? 'active' : ''}">
          <button
            class="module-button"
            data-module-id="${module.id}"
            aria-label="Módulo: ${module.title || 'Sem título'}"
            aria-expanded="${isActive}"
          >
            <span class="module-icon">📚</span>
            <span class="module-title">${module.title || 'Módulo'}</span>
          </button>
          <ul class="topics-list">
            ${topicsHtml}
          </ul>
        </li>
      `;
    })
    .join('');

  DOM.modulesList.innerHTML = html;

  // Attach event listeners to module buttons
  document.querySelectorAll('.module-button').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const moduleId = btn.dataset.moduleId;
      const module = appState.landingPageData.modules.find(m => m.id === moduleId);
      if (module?.topics?.[0]) {
        navigateTo(moduleId, module.topics[0].id, 1);
      }
      closeSidebarOnMobile();
    });
  });

  // Attach event listeners to topic buttons
  document.querySelectorAll('.topic-button').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const moduleId = btn.dataset.moduleId;
      const topicId = btn.dataset.topicId;
      const pageNum = parseInt(btn.dataset.page, 10);
      navigateTo(moduleId, topicId, pageNum);
      closeSidebarOnMobile();
    });
  });
}

/**
 * RENDERIZAÇÃO DE SLIDE
 */
function renderSlide() {
  if (!appState.landingPageData?.slides || Object.keys(appState.landingPageData.slides).length === 0) {
    showError('Nenhuma página disponível');
    return;
  }

  const slide = appState.landingPageData.slides[appState.currentSlideNumber];
  if (!slide) {
    showError('Página não encontrada');
    return;
  }

  // Verificar cache
  const cacheKey = `slide-${appState.currentSlideNumber}`;
  if (appState.slideCache[cacheKey]) {
    DOM.slideContent.innerHTML = appState.slideCache[cacheKey];
    DOM.slideLoading.style.display = 'none';
    DOM.slideContent.style.display = 'block';
    DOM.slideError.style.display = 'none';
    setupLazyLoading();
    updateSlideIndicators();
    updateNavigationButtons();
    return;
  }

  // Construir conteúdo HTML
  let contentHtml = `
    <div class="slide-header">
      <h2>${slide.title || `Slide ${appState.currentSlideNumber}`}</h2>
    </div>
  `;

  // Adicionar texto se disponível
  if (slide.content) {
    const textLines = slide.content
      .split('\n')
      .filter(line => line.trim())
      .map(line => `<p>${escapeHtml(line.trim())}</p>`)
      .join('');

    contentHtml += `<div class="slide-text">${textLines}</div>`;
  }

  // Adicionar imagens se disponível
  if (slide.images && Array.isArray(slide.images) && slide.images.length > 0) {
    contentHtml += '<div class="slide-images">';
    slide.images.forEach((img, idx) => {
      const imagePath = `./apostila_scraped/images/page-${appState.currentSlideNumber}-img-${img.index}.png`;
      contentHtml += `
        <figure class="slide-image-figure">
          <img
            class="lazy-image"
            src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='800' height='600'%3E%3Crect fill='%23f0f0f0' width='800' height='600'/%3E%3C/svg%3E"
            data-src="${imagePath}"
            alt="Imagem ${idx + 1} - ${slide.title}"
            loading="lazy"
          />
          <figcaption>Fig. ${idx + 1}: Imagem do slide</figcaption>
        </figure>
      `;
    });
    contentHtml += '</div>';
  }

  // Cache resultado
  appState.slideCache[cacheKey] = contentHtml;

  // Atualizar DOM
  DOM.slideContent.innerHTML = contentHtml;
  DOM.slideLoading.style.display = 'none';
  DOM.slideContent.style.display = 'block';
  DOM.slideError.style.display = 'none';

  // Configurar lazy loading
  setupLazyLoading();

  // Atualizar indicadores
  updateSlideIndicators();
  updateNavigationButtons();
  updatePageMeta();
}

/**
 * Exibir erro
 */
function showError(message) {
  DOM.slideError.innerHTML = `<p>${escapeHtml(message)}</p>`;
  DOM.slideLoading.style.display = 'none';
  DOM.slideContent.style.display = 'none';
  DOM.slideError.style.display = 'block';
}

/**
 * Escape HTML
 */
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

/**
 * LAZY LOADING DE IMAGENS COM INTERSECTIONOBSERVER
 */
function setupLazyLoading() {
  const images = document.querySelectorAll('.lazy-image');
  if (!images.length) return;

  if (appState.imageObserver) appState.imageObserver.disconnect();

  // Carregar imagens visíveis primeiro (eager)
  images.forEach((img, idx) => {
    if (idx < 3 || img.getBoundingClientRect().top < window.innerHeight) {
      const src = img.dataset.src;
      if (src) {
        img.src = src;
        img.onload = () => img.classList.add('loaded');
        img.onerror = () => img.classList.add('error');
      }
    }
  });

  // Observer para resto (lazy)
  appState.imageObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        const src = img.dataset.src;
        if (src && !img.src) {
          img.src = src;
          img.onload = () => img.classList.add('loaded');
          img.onerror = () => img.classList.add('error');
          appState.imageObserver.unobserve(img);
        }
      }
    });
  }, { rootMargin: '100px' });

  images.forEach(img => appState.imageObserver.observe(img));
}

/**
 * ATUALIZAR INDICADORES DE SLIDE
 */
function updateSlideIndicators() {
  const totalPages = appState.totalSlides;
  const currentPage = appState.currentSlideNumber;

  DOM.slideIndicator.textContent = `Slide ${currentPage} de ${totalPages}`;
  DOM.slideIndicator.setAttribute('aria-label', `Slide ${currentPage} de ${totalPages}`);

  const currentModule = appState.landingPageData?.modules?.find(m => m.id === appState.currentModuleId);
  const moduleTitle = currentModule?.title || 'Módulo';

  DOM.topicIndicator.textContent = `Módulo: ${moduleTitle}`;
  DOM.topicIndicator.setAttribute('aria-label', `Módulo: ${moduleTitle}`);
}

/**
 * ATUALIZAR BARRA DE PROGRESSO
 */
function updateProgressBar() {
  const totalPages = appState.totalSlides;
  const currentPage = appState.currentSlideNumber;
  const percentage = totalPages > 0 ? Math.round((currentPage / totalPages) * 100) : 0;

  const currentModule = appState.landingPageData?.modules?.find(m => m.id === appState.currentModuleId);
  const currentModuleIndex = appState.landingPageData?.modules?.indexOf(currentModule) + 1 || 1;
  const totalModules = appState.landingPageData?.modules?.length || 0;

  DOM.progressText.textContent = `Módulo ${currentModuleIndex} de ${totalModules}`;
  DOM.progressFill.style.width = `${percentage}%`;
  DOM.progressFill.parentElement.setAttribute('aria-valuenow', percentage);
}

/**
 * ATUALIZAR BOTÕES DE NAVEGAÇÃO
 */
function updateNavigationButtons() {
  const prevSlide = appState.currentSlideNumber - 1;
  const nextSlide = appState.currentSlideNumber + 1;
  const totalPages = appState.totalSlides;

  DOM.prevButton.disabled = prevSlide < 1;
  DOM.nextButton.disabled = nextSlide > totalPages;
}

/**
 * NAVEGAÇÃO ENTRE SLIDES
 */
function goToPreviousSlide() {
  if (appState.currentSlideNumber > 1) {
    navigateTo(appState.currentModuleId, appState.currentTopicId, appState.currentSlideNumber - 1);
  }
}

function goToNextSlide() {
  if (appState.currentSlideNumber < appState.totalSlides) {
    navigateTo(appState.currentModuleId, appState.currentTopicId, appState.currentSlideNumber + 1);
  }
}

/**
 * SEO DINÂMICO: Atualizar title, meta tags e canonical URL
 */
function updatePageMeta() {
  const slide = appState.landingPageData?.slides?.[appState.currentSlideNumber];
  if (!slide) return;

  const module = appState.landingPageData?.modules?.find(m => m.id === appState.currentModuleId);
  const title = `${slide.title} - ${module?.title || 'Apostila'} - Price Action`;
  const description = slide.content ? slide.content.substring(0, 160) : `Slide ${appState.currentSlideNumber}`;

  // Atualizar <title>
  document.title = title;

  // Atualizar ou criar meta tags
  setMetaTag('og:title', title);
  setMetaTag('og:description', description);
  setMetaTag('og:url', window.location.href);
  setMetaTag('description', description);

  // Canonical URL sempre aponta para slide-1 do tópico
  setCanonicalUrl(`/#/${appState.currentModuleId}/${appState.currentTopicId}/slide-1`);
}

/**
 * Define ou cria meta tag
 */
function setMetaTag(name, content) {
  let tag = document.querySelector(`meta[property="${name}"], meta[name="${name}"]`);
  if (!tag) {
    tag = document.createElement('meta');
    tag.setAttribute(name.startsWith('og:') ? 'property' : 'name', name);
    document.head.appendChild(tag);
  }
  tag.content = content;
}

/**
 * Define canonical URL
 */
function setCanonicalUrl(href) {
  let link = document.querySelector('link[rel="canonical"]');
  if (!link) {
    link = document.createElement('link');
    link.rel = 'canonical';
    document.head.appendChild(link);
  }
  link.href = `${window.location.origin}${window.location.pathname}${href}`;
}

/**
 * GERENCIAR TEMA (DARK/LIGHT)
 */
function initTheme() {
  const html = document.documentElement;
  html.setAttribute('data-theme', appState.theme);
  updateThemeButtonState();
}

function toggleTheme() {
  appState.theme = appState.theme === 'light' ? 'dark' : 'light';
  document.documentElement.setAttribute('data-theme', appState.theme);
  localStorage.setItem('theme', appState.theme);
  updateThemeButtonState();
}

function updateThemeButtonState() {
  const isDark = appState.theme === 'dark';
  DOM.themeToggle.setAttribute('aria-pressed', isDark);
  DOM.themeToggle.querySelector('.theme-icon').textContent = isDark ? '☀️' : '🌙';
  DOM.themeToggle.querySelector('.sr-only').textContent = `Tema atual: ${isDark ? 'Escuro' : 'Claro'}`;
}

/**
 * GERENCIAR SIDEBAR MOBILE
 */
function toggleSidebar() {
  const isExpanded = DOM.sidebarToggle.getAttribute('aria-expanded') === 'true';
  DOM.sidebarToggle.setAttribute('aria-expanded', !isExpanded);
  DOM.sidebar.classList.toggle('active');
}

function closeSidebarOnMobile() {
  if (window.innerWidth <= 768) {
    DOM.sidebarToggle.setAttribute('aria-expanded', 'false');
    DOM.sidebar.classList.remove('active');
  }
}

/**
 * INICIALIZAR VERSION INFO
 */
function initVersionInfo() {
  const versionText = window.landingPageData?.version || '1.0.0';
  const buildDate = new Date().toLocaleDateString('pt-BR');
  DOM.versionInfo.textContent = `v${versionText} — Build ${buildDate}`;
}

/**
 * EVENT LISTENERS
 */
function setupEventListeners() {
  // Tema
  DOM.themeToggle?.addEventListener('click', toggleTheme);

  // Sidebar
  DOM.sidebarToggle?.addEventListener('click', toggleSidebar);

  // Navegação de slides
  DOM.prevButton?.addEventListener('click', goToPreviousSlide);
  DOM.nextButton?.addEventListener('click', goToNextSlide);

  // Keyboard shortcuts
  document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft') goToPreviousSlide();
    if (e.key === 'ArrowRight') goToNextSlide();
  });

  // Hash change listener para sincronizar estado com URL
  window.addEventListener('hashchange', () => {
    if (parseRoute()) {
      renderModules();
      renderSlide();
      updateProgressBar();
    }
  });

  // Fechar sidebar ao clicar em um tópico (mobile)
  document.querySelectorAll('.topic-button').forEach(btn => {
    btn.addEventListener('click', closeSidebarOnMobile);
  });
}

/**
 * INICIALIZAÇÃO PRINCIPAL
 */
async function initialize() {
  console.log('Inicializando landing page SPA v2.0...');

  // 1. Inicializar DOM cache
  initDOMCache();

  // 2. Inicializar tema
  initTheme();

  // 3. Carregar dados
  const loaded = await loadLandingPageData();
  if (!loaded) {
    return; // Erro ao carregar dados
  }

  // 4. Parse rota inicial (hash-based)
  if (!parseRoute()) {
    return; // Erro ao processar rota
  }

  // 5. Renderizar UI
  renderModules();
  renderSlide();
  updateProgressBar();

  // 6. Setup listeners (inclui hashchange)
  setupEventListeners();

  // 7. Versão info
  initVersionInfo();

  console.log('✓ Landing page SPA inicializada com sucesso');
  console.log(`  URL atual: ${window.location.hash}`);
  console.log(`  Slide: ${appState.currentSlideNumber} / ${appState.totalSlides}`);
}

/**
 * BOOT
 * Primeiro verificar autenticação, depois inicializar
 */
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', checkAuthentication);
} else {
  checkAuthentication();
}
