# Método Price Action — Landing Page Educacional

Uma plataforma web educacional interativa que apresenta o **Método Price Action** desenvolvido por **Oliver Velez**, em uma compilação organizada por **André Trader**.

## Características

✨ **Recursos Principais**

- 📚 **Estrutura Modular**: Conteúdo organizado em módulos e tópicos
- 🎨 **Tema Adaptável**: Alternância entre modo claro e escuro
- 📱 **Responsivo**: Funciona perfeitamente em desktop, tablet e mobile
- ⌨️ **Navegação Fluida**: Setas do teclado, botões e sidebar interativa
- 📊 **Barra de Progresso**: Acompanhamento visual do progresso de aprendizado
- 🖼️ **Suporte a Imagens**: Exibição de gráficos, diagramas e exemplos técnicos
- ♿ **Acessível**: Semântica HTML5, ARIA labels e navegação por teclado

## Tech Stack

| Tecnologia | Função |
|-----------|--------|
| **HTML5** | Estrutura semântica |
| **CSS3** | Design responsivo, variáveis CSS, dark mode |
| **JavaScript (Vanilla)** | Interatividade sem dependências |
| **JSON** | Armazenamento de dados de conteúdo |

## Estrutura de Arquivos

```
price-action-landing-page/
├── index.html                          # Estrutura HTML principal
├── style.css                           # Estilos (light/dark theme)
├── app.js                              # Lógica de aplicação
├── apostila_scraped/
│   ├── landing-page-data.json         # Dados consolidados (módulos, slides, imagens)
│   ├── images-webp/                   # Imagens otimizadas em WebP
│   └── images-fallback/               # Fallback PNG/JPG para navegadores antigos
├── README.md                           # Este arquivo
├── CHANGELOG.md                        # Histórico de versões
└── .gitignore                          # Configuração de Git
```

## Como Usar

### Desenvolvimento Local

1. **Clonar repositório**
   ```bash
   git clone https://github.com/[seu-usuario]/price-action-landing-page.git
   cd price-action-landing-page
   ```

2. **Servir localmente** (qualquer servidor HTTP funciona)
   ```bash
   # Python 3
   python -m http.server 8000
   
   # Node.js (http-server)
   npx http-server
   
   # VS Code Live Server
   # Extensão: ritwickdey.LiveServer
   ```

3. **Acessar em browser**
   ```
   http://localhost:8000
   ```

### Navegação

| Ação | Como Fazer |
|------|-----------|
| Próximo slide | Seta direita (→) ou botão "Próximo" |
| Slide anterior | Seta esquerda (←) ou botão "Anterior" |
| Mudar tema | Botão 🌙/☀️ no header |
| Abrir sidebar | Botão ☰ (mobile) |
| Selecionar módulo | Clique na sidebar |

## Deploy em GitHub Pages

### Setup Automático

1. **Criar repositório** no GitHub
   ```bash
   gh repo create price-action-landing-page --public --source=. --remote=origin --push
   ```

2. **Configurar GitHub Pages**
   - Ir em **Settings** → **Pages**
   - Source: `main` branch, root directory
   - Salvar

3. **Site estará live em:**
   ```
   https://[seu-usuario].github.io/price-action-landing-page/
   ```

### Publicação de Atualizações

```bash
git add .
git commit -m "feat: descrição da mudança"
git push origin main
```

Deploy automático em segundos! ✨

## Performance & Otimizações

- 🖼️ **Imagens WebP** com fallback PNG/JPG
- 🗜️ **CSS e JS minificados**
- ⚡ **Lazy loading** de imagens
- 🎯 **Cache busting** via versionamento
- 📦 **Zero dependências** externas

**Pontuação Lighthouse alvo:**
- Performance: ≥90
- Accessibility: ≥90
- Best Practices: ≥90
- SEO: ≥90

## Créditos

| Papel | Pessoa |
|------|--------|
| **Método** | Oliver Velez (iFund Traders) |
| **Compilação** | André Trader |
| **Plataforma** | FIMATHE Trading Education |
| **Desenvolvimento** | Claude AI (Anthropic) |

## Licença

Este projeto é **educacional** e segue as políticas da FIMATHE. 

**Importante:** O método Price Action é propriedade intelectual de Oliver Velez. Este material é fornecido para fins educacionais apenas.

## Suporte

Encontrou um problema ou tem uma sugestão?

- 📧 Email: [seu-email@exemplo.com]
- 🐛 Issues: GitHub Issues
- 💬 Discussões: GitHub Discussions

## Roadmap

- [ ] PWA (Progressive Web App)
- [ ] Testes interativos
- [ ] Quiz e avaliação
- [ ] Certificado digital
- [ ] API para tracking de progresso
- [ ] Integração com plataforma LMS

---

**Última atualização:** 2026-04-24  
**Versão:** 1.0.0  
**Status:** ✅ Em produção
