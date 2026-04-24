# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/),
e este projeto adere a [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [1.0.0] - 2026-04-24

### Adicionado

- ✨ **Landing page interativa** com suporte a light/dark theme
- 📚 **Estrutura modular** com 5 módulos de conteúdo
- 🎨 **Design responsivo** otimizado para mobile, tablet e desktop
- ⌨️ **Navegação fluida**
  - Setas do teclado (← / →)
  - Botões anterior/próximo
  - Sidebar com módulos e tópicos
- 📊 **Barra de progresso** com indicadores de avanço
- 🖼️ **Suporte a imagens** com lazy loading
  - Fallback WebP + PNG/JPG
  - Legendas e figcaptions
  - Otimização automática
- ♿ **Acessibilidade completa**
  - Semântica HTML5 apropriada
  - ARIA labels em todos os controles
  - Navegação por teclado
  - Skip links
  - Indicadores de progresso com aria-live
- 🌓 **Tema dark/light**
  - Persistência em localStorage
  - Variáveis CSS para fácil customização
  - Transições suaves
- 📱 **Menu mobile** com sidebar colapsável
- 💾 **Zero dependências** — HTML5 + CSS3 + Vanilla JavaScript
- 📈 **SEO otimizado**
  - Meta tags completas
  - Open Graph (og:title, og:description, og:type)
  - Canonical URLs
  - Structured data pronto

### Detalhes Técnicos

#### HTML (index.html)
- Estrutura semântica com `<header>`, `<main>`, `<aside>`, `<footer>`
- Suporte a ARIA labels e roles
- Preload de fontes Inter
- Meta tags de viewport e SEO

#### CSS (style.css)
- Sistema de variáveis CSS (--text-primary, --bg-primary, etc.)
- Media queries responsivas
- Dark mode automático com `[data-theme="dark"]`
- Flexbox e Grid layouts
- Tipografia Inter com fallbacks
- Transições suaves (0.3s)

#### JavaScript (app.js)
- Carregamento dinâmico de JSON (`landing-page-data.json`)
- Renderização de módulos e slides
- Gerenciamento de estado com `appState`
- Cache de DOM elements
- Event listeners para navegação
- Keyboard shortcuts (ArrowLeft, ArrowRight)
- Lazy loading de imagens

#### Dados (apostila_scraped/landing-page-data.json)
- Consolidação de 350 páginas PDF
- 877 imagens processadas
- Estrutura hierárquica: Módulos → Tópicos → Páginas
- Metadados: títulos, subtítulos, captions

### Performance

- Lighthouse Score alvo: ≥90 em todos critérios
- Imagens WebP com fallback PNG/JPG
- CSS e JS minificáveis
- Zero dependências externas
- Carregamento assíncrono do JSON

### Navegadores Suportados

| Navegador | Versão |
|-----------|--------|
| Chrome | ≥90 |
| Firefox | ≥88 |
| Safari | ≥14 |
| Edge | ≥90 |
| Mobile Chrome | ≥90 |
| Mobile Safari | ≥14 |

### Conhecidos / TODO

- ⏳ PWA (Progressive Web App) — próxima versão
- ⏳ Quiz e testes interativos — roadmap v2.0
- ⏳ Certificado digital — roadmap v3.0
- ⏳ Integração LMS — roadmap v3.0

---

## Versionamento

Este projeto segue [Semantic Versioning](https://semver.org/lang/pt-BR/):

- **MAJOR** (X.0.0): Mudanças incompatíveis na API
- **MINOR** (0.X.0): Novas funcionalidades compatíveis
- **PATCH** (0.0.X): Correções de bugs

Exemplo: **1.0.0**
- 1 = MAJOR (versão estável)
- 0 = MINOR (sem novas features)
- 0 = PATCH (sem bug fixes)

---

## Créditos

| Papel | Pessoa/Organização |
|------|------------------|
| Método Price Action | Oliver Velez (iFund Traders) |
| Compilação | André Trader |
| Plataforma Educacional | FIMATHE Trading Education |
| Desenvolvimento | Claude AI (Anthropic) |

---

**Última atualização:** 2026-04-24  
**Mantenedor:** [seu-usuario@github.com]
