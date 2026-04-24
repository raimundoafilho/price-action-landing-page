# GitHub Pages Deploy Guide — Landing Page Price Action

## Status Atual

✅ **Todos os arquivos prontos para deploy**

```
C:\PROJETO-IA\TRADE\
├── index.html                      (7 KB) ✅
├── app.js                          (21 KB) ✅
├── style.css                       (42 KB) ✅
├── README.md                       ✅
├── CHANGELOG.md                    ✅
├── DEPLOYMENT_SUMMARY.md           ✅ (Novo)
├── .gitignore                      ✅
├── .git/                           ✅ (Repositório inicializado)
└── apostila_scraped/
    └── landing-page-data.json      (297 KB) ✅
```

---

## 📋 Passos para Deploy

### Passo 1: Fazer Commit Final (Se não feito)

```bash
cd C:\PROJETO-IA\TRADE

# Verificar status
git status

# Ver arquivos não commitados
git log --oneline -1

# Se necessário, fazer commit final
git add DEPLOYMENT_SUMMARY.md ALTERACOES_DETALHADAS.txt CHECKLIST_VERIFICACAO.md
git commit -m "feat: Landing page Price Action pronta para GitHub Pages deploy"
```

**O que esperar:**
```
[master xxxxx] feat: Landing page Price Action pronta para GitHub Pages deploy
 3 files changed, 500 insertions(+)
 create mode 100644 DEPLOYMENT_SUMMARY.md
 ...
```

---

### Passo 2: Criar Repositório no GitHub

1. Acesse: https://github.com/new
2. Preencha:
   - **Repository name:** `price-action-landing-page`
   - **Description:** "Landing page educacional do Método Price Action - Oliver Velez"
   - **Visibility:** Public (necessário para GitHub Pages)
   - **Initialize:** Deixar em branco (já temos .git localmente)
3. Clique em "Create repository"

---

### Passo 3: Conectar Repositório Local ao GitHub

**Depois de criar o repositório, GitHub mostrará comandos. Use:**

```bash
cd C:\PROJETO-IA\TRADE

# Adicionar remote (substitua USERNAME pelo seu username GitHub)
git remote add origin https://github.com/USERNAME/price-action-landing-page.git

# Renomear branch de master para main (se necessário)
git branch -M main

# Fazer push do conteúdo
git push -u origin main
```

**O que esperar:**
```
Enumerating objects: XX, done.
Counting objects: 100% (XX/XX), done.
Delta compression using up to 4 threads
Compressing objects: 100% (XX/XX), done.
Writing objects: 100% (XX/XX), done.
...
To https://github.com/USERNAME/price-action-landing-page.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

---

### Passo 4: Ativar GitHub Pages

**Automático:** GitHub detecta `index.html` na raiz da branch `main` e ativa Pages automaticamente.

**Para verificar/configurar manualmente:**

1. Vá para: https://github.com/USERNAME/price-action-landing-page/settings
2. Procure por "Pages" no menu esquerdo
3. Verifique:
   - **Source:** "Deploy from a branch"
   - **Branch:** main
   - **Folder:** / (root)
4. Se não estiver ativado, configure e salve

---

### Passo 5: Validar Deploy

Após 30-60 segundos, sua página estará ao vivo em:

```
https://USERNAME.github.io/price-action-landing-page/
```

**Validação:**
1. Acesse a URL acima
2. Você verá a tela de login
3. Digite a senha: `AndreTrader`
4. Verifique:
   - ✅ Login aceita a senha
   - ✅ Landing page carrega sem erros
   - ✅ Módulos e tópicos aparecem
   - ✅ Navegação funciona
   - ✅ JSON `landing-page-data.json` carrega
   - ✅ Console do browser (F12) não mostra erros

---

## 🔍 Troubleshooting

### Problema: "404 - Not Found"
- **Causa:** GitHub Pages ainda não ativou (espere 1-2 minutos)
- **Solução:** Recarregue a página após 1 minuto

### Problema: "GitHub Pages is not enabled"
- **Causa:** Repositório é privado ou branch wrong
- **Solução:** 
  1. Vá em Settings → Pages
  2. Mude visibilidade para Public (se privado)
  3. Configure branch como `main`

### Problema: "index.html não encontrado"
- **Causa:** `index.html` não está na raiz
- **Solução:** Verifique `git ls-files | grep index.html`
- **Resultado esperado:** `index.html` (sem caminho)

### Problema: Login não funciona
- **Causa:** `app.js` não carregou ou erro JavaScript
- **Solução:** 
  1. Abra F12 (DevTools)
  2. Vá para "Console"
  3. Procure por erros em vermelho
  4. Verifique se `app.js` está no path correto

### Problema: Dados não carregam (JSON vazio)
- **Causa:** `landing-page-data.json` não encontrado
- **Solução:**
  1. Verifique se arquivo existe: `git ls-files | grep landing-page-data.json`
  2. Caminho esperado: `apostila_scraped/landing-page-data.json`
  3. Se não existir, faça push novamente

### Problema: Imagens não aparecem
- **Causa:** `images-webp/` ou `images-fallback/` vazia
- **Solução:** Processar e adicionar imagens (veja Passo 6)

---

## Passo 6: Adicionar Imagens (Opcional - Para Versão Final)

Se tiver imagens a adicionar:

```bash
cd C:\PROJETO-IA\TRADE

# 1. Colocar imagens WebP em apostila_scraped/images-webp/
# 2. Colocar imagens PNG em apostila_scraped/images-fallback/

# 3. Atualizar landing-page-data.json com referências

# 4. Fazer commit
git add apostila_scraped/images-webp/ apostila_scraped/images-fallback/
git commit -m "feat: Adicionar imagens otimizadas para landing page"

# 5. Push para GitHub
git push origin main
```

---

## ✅ Checklist Final

- [ ] Repositório GitHub criado
- [ ] Remote adicionado localmente (`git remote -v`)
- [ ] Push realizado (`git log --oneline` mostra commits)
- [ ] GitHub Pages ativado (Settings → Pages)
- [ ] URL ativa: `https://USERNAME.github.io/price-action-landing-page/`
- [ ] Login funciona com `AndreTrader`
- [ ] Landing page carrega sem erros
- [ ] Lighthouse score ≥ 85
- [ ] Responsividade OK (testar em mobile)
- [ ] Documentação atualizada

---

## 📊 Performance Esperado

| Métrica | Target | Método de Teste |
|---------|--------|-----------------|
| Page Load | < 3s | DevTools Network tab |
| Login Response | < 100ms | F12 → Console |
| JSON Load | < 1s | Network tab, filter XHR |
| Lighthouse | ≥ 85 | https://PageSpeed.web.dev |

---

## 🔐 Segurança

### Autenticação Básica
- **Tipo:** Client-side (sessionStorage)
- **Senha:** `AndreTrader`
- **Validade:** Sessão (recarregar = re-autenticar)
- **Nível:** Baixo (adequado para ambiente educacional restrito)

### Para Produção (Futuro)
Se precisar de autenticação mais robusta:
- Implementar backend com JWT
- Hash de senhas com bcrypt
- Rate limiting de login
- Logs de acesso

---

## 📞 Suporte GitHub Pages

- **Documentação:** https://docs.github.com/en/pages
- **Status:** https://www.githubstatus.com/
- **Comunidade:** https://github.com/github/pages/discussions

---

*Guia criado em 2026-04-24*  
*Pronto para deploy imediato*
