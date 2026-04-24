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
    return true;
  } catch (e) {
    console.error('Erro ao carregar JSON:', e);
    alert('Erro ao carregar dados: ' + e.message);
    return false;
  }
}

function submitPassword() {
  const pwd = document.getElementById('passwordInput').value;
  const error = document.getElementById('loginError');

  if (pwd === CORRECT_PASSWORD) {
    sessionStorage.setItem('authenticated', 'true');
    showApp();
  } else {
    error.textContent = '❌ Senha incorreta. Tente novamente.';
    document.getElementById('passwordInput').value = '';
    document.getElementById('passwordInput').focus();
  }
}

function showApp() {
  document.getElementById('login-screen').style.display = 'none';
  document.getElementById('slideContainer').style.display = 'block';
  initializeApp();
}

async function initializeApp() {
  if (!appData) {
    const loaded = await loadData();
    if (!loaded) return;
  }

  renderModules();
  renderSlide();
}

function renderModules() {
  const list = document.getElementById('modulesList');
  if (!list || !appData) return;

  list.innerHTML = '';

  appData.modules.forEach((mod, idx) => {
    const li = document.createElement('li');
    li.className = 'module-item';
    if (idx === currentModule) li.classList.add('active');

    const button = document.createElement('button');
    button.textContent = mod.title;
    button.onclick = () => selectModule(idx);

    li.appendChild(button);
    list.appendChild(li);
  });
}

function selectModule(idx) {
  currentModule = idx;
  currentTopic = 0;
  currentSlide = 0;
  renderModules();
  renderSlide();
}

function renderSlide() {
  if (!appData || !appData.modules[currentModule]) return;

  const mod = appData.modules[currentModule];
  const topics = mod.topics || [];
  const topic = topics[currentTopic];
  const slides = topic?.slides || [];
  const slide = slides[currentSlide];

  // Renderizar conteúdo
  const content = document.getElementById('slideContent');
  if (content && slide) {
    content.innerHTML = `
      <h2>${slide.title}</h2>
      <div>${slide.content || ''}</div>
    `;
  }

  // Atualizar indicadores
  document.getElementById('slideIndicator').textContent =
    `Slide ${currentSlide + 1} de ${slides.length}`;
  document.getElementById('topicIndicator').textContent =
    `Módulo: ${mod.title}`;
  document.getElementById('progressText').textContent =
    `Módulo ${currentModule + 1} de ${appData.modules.length}`;

  // Atualizar botões
  document.getElementById('prevButton').disabled = (currentSlide === 0 && currentModule === 0);
  document.getElementById('nextButton').disabled =
    (currentSlide === slides.length - 1 && currentModule === appData.modules.length - 1);
}

function goToPrevious() {
  if (currentSlide > 0) {
    currentSlide--;
  } else if (currentModule > 0) {
    currentModule--;
    const topics = appData.modules[currentModule].topics || [];
    const slides = topics[topics.length - 1]?.slides || [];
    currentSlide = Math.max(0, slides.length - 1);
  }
  renderModules();
  renderSlide();
}

function goToNext() {
  const mod = appData.modules[currentModule];
  const topics = mod.topics || [];
  const topic = topics[currentTopic];
  const slides = topic?.slides || [];

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
}

// Inicializar ao carregar
window.addEventListener('DOMContentLoaded', () => {
  const theme = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-theme', theme);

  const isAuth = sessionStorage.getItem('authenticated') === 'true';
  if (isAuth) {
    showApp();
  } else {
    document.getElementById('passwordInput')?.focus();
  }

  // Event listeners
  document.getElementById('themeToggle')?.addEventListener('click', toggleTheme);
  document.getElementById('prevButton')?.addEventListener('click', goToPrevious);
  document.getElementById('nextButton')?.addEventListener('click', goToNext);
  document.getElementById('passwordInput')?.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') submitPassword();
  });
});
