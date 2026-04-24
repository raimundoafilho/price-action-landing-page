'use strict';

const CORRECT_PASSWORD = 'AndreTrader';
let appData = null;
let currentModule = 0;
let currentTopic = 0;
let currentSlide = 0;

async function loadData() {
  try {
    const res = await fetch('./apostila_scraped/landing-page-data.json');
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    appData = await res.json();
    console.log('JSON carregado:', appData.modules?.length, 'módulos');
    return true;
  } catch (e) {
    console.error('Erro ao carregar JSON:', e);
    alert('Erro ao carregar dados: ' + e.message);
    return false;
  }
}

function submitPassword() {
  const pwd = document.getElementById('passwordInput')?.value || '';
  const error = document.getElementById('loginError');

  console.log('Tentando login com:', pwd);

  if (pwd === CORRECT_PASSWORD) {
    sessionStorage.setItem('authenticated', 'true');
    showApp();
  } else {
    if (error) error.textContent = 'Senha incorreta. Tente novamente.';
    const input = document.getElementById('passwordInput');
    if (input) {
      input.value = '';
      input.focus();
    }
  }
}

function showApp() {
  const login = document.getElementById('login-screen');
  const container = document.getElementById('slideContainer');

  if (login) login.style.display = 'none';
  if (container) container.style.display = 'block';

  initializeApp();
}

async function initializeApp() {
  console.log('Inicializando app...');

  if (!appData) {
    const loaded = await loadData();
    if (!loaded) return;
  }

  renderModules();
  renderSlide();
}

function renderModules() {
  console.log('Renderizando módulos...');
  const list = document.getElementById('modulesList');

  if (!list) {
    console.error('modulesList não encontrado');
    return;
  }

  if (!appData || !appData.modules) {
    console.error('appData ou modules não disponível');
    return;
  }

  list.innerHTML = '';

  appData.modules.forEach((mod, idx) => {
    const li = document.createElement('li');
    li.className = 'module-item';
    if (idx === currentModule) li.classList.add('active');

    const button = document.createElement('button');
    button.textContent = mod.title || `Módulo ${idx + 1}`;
    button.onclick = () => {
      currentModule = idx;
      currentTopic = 0;
      currentSlide = 0;
      renderModules();
      renderSlide();
    };

    li.appendChild(button);
    list.appendChild(li);
  });

  console.log('Módulos renderizados:', appData.modules.length);
}

function renderSlide() {
  console.log('Renderizando slide...');

  if (!appData || !appData.modules || !appData.modules[currentModule]) {
    console.error('Dados inválidos para renderizar slide');
    return;
  }

  const mod = appData.modules[currentModule];
  const topics = mod.topics || [];
  const topic = topics[currentTopic] || topics[0];

  if (!topic) {
    console.error('Nenhum tópico disponível');
    return;
  }

  const slides = topic.slides || [];
  const slide = slides[currentSlide] || slides[0];

  if (!slide) {
    console.error('Nenhum slide disponível');
    return;
  }

  // Renderizar conteúdo
  const content = document.getElementById('slideContent');
  if (content) {
    content.innerHTML = `
      <h2>${slide.title || 'Slide'}</h2>
      <div class="slide-body">${slide.content || 'Sem conteúdo'}</div>
    `;
  }

  // Atualizar indicadores
  const slideInd = document.getElementById('slideIndicator');
  if (slideInd) slideInd.textContent = `Slide ${currentSlide + 1} de ${slides.length}`;

  const topicInd = document.getElementById('topicIndicator');
  if (topicInd) topicInd.textContent = `${mod.title}`;

  const progress = document.getElementById('progressText');
  if (progress) progress.textContent = `Módulo ${currentModule + 1} de ${appData.modules.length}`;

  // Atualizar botões
  const prevBtn = document.getElementById('prevButton');
  const nextBtn = document.getElementById('nextButton');

  if (prevBtn) prevBtn.disabled = (currentSlide === 0 && currentModule === 0);
  if (nextBtn) nextBtn.disabled = (currentSlide === slides.length - 1 && currentModule === appData.modules.length - 1);

  console.log('Slide renderizado:', slide.title);
}

function goToPrevious() {
  const mod = appData.modules[currentModule];
  const topics = mod.topics || [];
  const slides = (topics[currentTopic]?.slides || []);

  if (currentSlide > 0) {
    currentSlide--;
  } else if (currentModule > 0) {
    currentModule--;
    const prevMod = appData.modules[currentModule];
    const prevTopics = prevMod.topics || [];
    const prevSlides = (prevTopics[0]?.slides || []);
    currentSlide = Math.max(0, prevSlides.length - 1);
  }

  renderModules();
  renderSlide();
}

function goToNext() {
  const mod = appData.modules[currentModule];
  const topics = mod.topics || [];
  const slides = (topics[currentTopic]?.slides || []);

  if (currentSlide < slides.length - 1) {
    currentSlide++;
  } else if (currentModule < appData.modules.length - 1) {
    currentModule++;
    currentTopic = 0;
    currentSlide = 0;
  }

  renderModules();
  renderSlide();
}

function logout() {
  if (confirm('Deseja sair?')) {
    sessionStorage.removeItem('authenticated');
    location.reload();
  }
}

function toggleTheme() {
  const html = document.documentElement;
  const isDark = html.getAttribute('data-theme') === 'dark';
  html.setAttribute('data-theme', isDark ? 'light' : 'dark');
  localStorage.setItem('theme', isDark ? 'light' : 'dark');

  const icon = document.querySelector('.theme-icon');
  if (icon) icon.textContent = isDark ? '🌙' : '☀️';
}

// Inicializar ao carregar
window.addEventListener('DOMContentLoaded', () => {
  console.log('DOM carregado, inicializando...');

  const theme = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-theme', theme);

  const isAuth = sessionStorage.getItem('authenticated') === 'true';
  console.log('Autenticado?', isAuth);

  if (isAuth) {
    showApp();
  } else {
    const input = document.getElementById('passwordInput');
    if (input) input.focus();
  }

  // Event listeners
  const themeBtn = document.getElementById('themeToggle');
  if (themeBtn) themeBtn.addEventListener('click', toggleTheme);

  const prevBtn = document.getElementById('prevButton');
  if (prevBtn) prevBtn.addEventListener('click', goToPrevious);

  const nextBtn = document.getElementById('nextButton');
  if (nextBtn) nextBtn.addEventListener('click', goToNext);

  const input = document.getElementById('passwordInput');
  if (input) {
    input.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') submitPassword();
    });
  }

  console.log('Inicialização completa');
});
