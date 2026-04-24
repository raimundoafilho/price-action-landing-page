# 🧪 GUIA COMPLETO DE TESTES LOCAIS - Landing Page Price Action

## 📋 SUMÁRIO

1. ✅ Teste Local (sem GitHub)
2. ✅ Teste do Login
3. ✅ Teste de Navegação
4. ✅ Teste de Responsividade
5. ✅ Teste de Performance
6. ✅ Teste de Acessibilidade

---

## 🚀 PARTE 1: INICIAR SERVIDOR LOCAL

### Opção A: Python (Recomendado - Mais fácil)

```bash
cd C:\PROJETO-IA\TRADE

# Python 3.x
python -m http.server 8000

# OU Python 2.x
python -m SimpleHTTPServer 8000
```

**Esperado:**
```
Serving HTTP on 0.0.0.0 port 8000 (http://127.0.0.1:8000/) ...
```

### Opção B: Node.js (Se tiver instalado)

```bash
cd C:\PROJETO-IA\TRADE

# Instalar http-server (uma vez)
npm install -g http-server

# Iniciar
http-server
```

**Esperado:**
```
Hit CTRL-C to stop the server
[ Thu Apr 24 2026 14:30:00 GMT-0300 (Brasília Time) ]
HTTP server is running at:
  http://127.0.0.1:8080
```

### Opção C: PowerShell (Windows nativo)

```powershell
cd C:\PROJETO-IA\TRADE

# Iniciar servidor simples
python -m http.server 8000
```

---

## ✅ PARTE 2: ABRIR NO NAVEGADOR

### Acesso Local

**URL:** `http://localhost:8000`

OU

**URL:** `http://127.0.0.1:8000`

---

## 🔐 PARTE 3: TESTAR LOGIN

### Teste 1: Tela de Login Aparece?

**Esperado:**
```
[Tela escura com caixa branca no centro]
├─ Título: "Método Price Action"
├─ Subtítulo: "Oliver Velez | André Trader"
├─ Descrição: "Plataforma Educacional Restrita"
├─ Campo de senha: "Digite a senha para acessar"
└─ Botão: "🔓 Entrar"
```

**Se NÃO aparecer:**
- ❌ Abra DevTools: `F12`
- ❌ Vá em Console (aba vermelha?)
- ❌ Procure por erros
- ❌ Verifique se `landing-page-data.json` existe

---

### Teste 2: Senha Correta

**Digite:** `AndreTrader`  
**Clique:** "🔓 Entrar"

**Esperado:**
```
[Tela de login some]
[Landing page aparece com:
├─ Header: "Método Price Action" + toggle tema
├─ Sidebar: Módulos listados
├─ Centro: Slide 1 do Módulo 1
└─ Rodapé: Botões Anterior/Próximo
]
```

**Se NÃO funcionar:**
- ❌ Verifique senha (case-sensitive)
- ❌ Abra DevTools: `F12`
- ❌ Console mostra erro?
- ❌ Teste com `AndreTrader` exatamente

---

### Teste 3: Senha Incorreta

**Digite:** `senhaerrada`  
**Clique:** "🔓 Entrar"

**Esperado:**
```
❌ Mensagem: "Senha incorreta. Tente novamente."
[Campo limpo, focus retorna ao input]
```

**Se NÃO aparecer:**
- ❌ Abra Console (F12)
- ❌ Procure por erro em `submitPassword()`

---

## 📚 PARTE 4: TESTAR NAVEGAÇÃO

### Teste 4: Clique em Módulo

**Ação:** Clique em qualquer módulo na sidebar (ex: "Módulo Básico 2")

**Esperado:**
```
✅ Slide muda para Slide 1 daquele módulo
✅ Título muda
✅ Conteúdo muda
✅ Módulo fica destacado na sidebar
✅ Indicador em baixo mostra: "Slide 1 de X"
```

---

### Teste 5: Botão "Próximo"

**Ação:** Clique botão "Próximo →" no rodapé

**Esperado:**
```
✅ Slide avança (1 → 2 → 3...)
✅ Conteúdo muda
✅ Indicador mostra slide correto
✅ Botão "Anterior" fica habilitado
```

---

### Teste 6: Botão "Anterior"

**Ação:** Clique botão "← Anterior" no rodapé

**Esperado:**
```
✅ Slide volta (3 → 2 → 1...)
✅ Conteúdo muda
✅ Indicador mostra slide correto
```

---

### Teste 7: Limites de Navegação

**Ação:** Estando no Slide 1, clique "← Anterior"

**Esperado:**
```
❌ Botão "Anterior" DESABILITADO (cinza)
✅ Não volta além do Slide 1
```

**Ação:** Estando no último slide, clique "Próximo →"

**Esperado:**
```
❌ Botão "Próximo" DESABILITADO (cinza)
✅ Não avança além do último slide
```

---

### Teste 8: Tema Dark/Light

**Ação:** Clique botão 🌙 no header

**Esperado:**
```
✅ Tema muda de claro para escuro (ou vice-versa)
✅ Cores se invertem
✅ Ícone muda (🌙 ↔ ☀️)
✅ Logo "Dark Mode" salvo em localStorage
```

**Ação:** Recarregue página (F5)

**Esperado:**
```
✅ Tema mantém-se escuro/claro (persistente)
```

---

### Teste 9: Expandir Módulos

**Ação:** Clique na seta/chevron de um módulo (se tiver)

**Esperado:**
```
✅ Subtópicos aparecem/desaparecem
✅ Seta gira
```

---

## 📱 PARTE 5: TESTAR RESPONSIVIDADE

### Teste 10: Desktop (Tela Grande)

**Ação:** Abra em tela cheia do navegador (máximo)

**Esperado:**
```
✅ Layout horizontal:
  ├─ Sidebar fixa à esquerda (250px)
  ├─ Conteúdo central (expansível)
  └─ Rodapé na base
✅ Imagens visíveis, texto legível
✅ Sem overflow horizontal
```

---

### Teste 11: Tablet (768px - 1024px)

**Método 1: DevTools do Chrome**
```
1. Abra Chrome
2. Pressione: F12
3. Clique: Device Toggle (Ctrl+Shift+M)
4. Selecione: iPad (768x1024)
5. Verifique layout
```

**Método 2: Redimensione janela**
```
1. Redimensione seu navegador
2. Deixe com ~900px de largura
3. Observe mudanças
```

**Esperado:**
```
✅ Sidebar colapsável (hamburger menu aparece)
✅ Conteúdo se expande
✅ Botões reduzem tamanho
✅ Imagens redimensionam
```

---

### Teste 12: Mobile (< 768px)

**DevTools:** Ctrl+Shift+M → Selecione "iPhone 12" (390x844)

**Esperado:**
```
✅ Sidebar some (menu hamburger ☰ aparece)
✅ Conteúdo ocupa 100% width
✅ Texto reduz (13px → 12px)
✅ Botões empilhados verticalmente
✅ Imagens 100% width com padding
✅ Sem scroll horizontal
```

---

## ⚡ PARTE 6: TESTAR PERFORMANCE

### Teste 13: Velocidade de Carregamento

**DevTools:** F12 → Aba "Network"

**Ação:** Recarregue página (F5)

**Esperado:**
```
✅ index.html: < 50ms
✅ app.js: < 100ms
✅ style.css: < 50ms
✅ landing-page-data.json: < 500ms (maior arquivo)
✅ Total: < 2 segundos
```

**Se > 2s:**
- ❌ Verifique internet (conexão lenta?)
- ❌ Verifique arquivo JSON (muito grande?)

---

### Teste 14: Lazy Loading de Imagens

**DevTools:** F12 → Aba "Network" → Filtre "img"

**Ação:** Navegue pelos slides, scroll down

**Esperado:**
```
✅ Imagens carregam sob demanda
✅ Não carregam todas de uma vez
✅ Performance não degrada
```

---

### Teste 15: Lighthouse Score

**DevTools:** F12 → Aba "Lighthouse"

**Ação:** 
1. Clique "Analyze page load"
2. Aguarde ~30 segundos

**Esperado:**
```
✅ Performance: ≥ 85
✅ Accessibility: ≥ 90
✅ Best Practices: ≥ 85
✅ SEO: ≥ 90
```

**Se < 85:**
- ⚠️ Verifique console para warnings
- ⚠️ Otimize imagens se necessário

---

## ♿ PARTE 7: TESTAR ACESSIBILIDADE

### Teste 16: Navegação por Teclado

**Ação:** Pressione TAB repetidamente

**Esperado:**
```
✅ Foco percorre:
  1. Botão tema
  2. Sidebar (se visível)
  3. Links de módulos
  4. Botão Anterior
  5. Botão Próximo
✅ Outline azul/dourado visível em cada elemento
```

---

### Teste 17: Enter para Submeter

**Ação:** 
1. No login, pressione TAB até o campo de senha
2. Digite: `AndreTrader`
3. Pressione: ENTER

**Esperado:**
```
✅ Login funciona sem clicar botão
✅ Landing page abre
```

---

### Teste 18: Alt Text em Imagens

**DevTools:** F12 → Aba "Elements"

**Ação:** Inspecione uma imagem (clique direito → Inspect)

**Esperado:**
```
✅ <img alt="descrição clara da imagem">
✅ Toda imagem tem alt text (não vazio)
```

---

### Teste 19: Contraste de Cores

**Ferramenta Online:** https://webaim.org/resources/contrastchecker/

**Ação:** 
1. Abra a ferramenta
2. Pegue uma cor do seu site (ex: #1a3a52 texto, #ffffff fundo)
3. Coloque na ferramenta

**Esperado:**
```
✅ Ratio: ≥ 4.5:1 (AA Compliance)
```

---

## 📋 CHECKLIST COMPLETO DE TESTES

### Login
- [ ] Tela de login aparece ao abrir
- [ ] Senha `AndreTrader` funciona
- [ ] Senha incorreta mostra erro
- [ ] Campo limpa após erro

### Navegação
- [ ] Clique em módulo abre corretamente
- [ ] Botão "Próximo" avança slides
- [ ] Botão "Anterior" volta slides
- [ ] Botões desabilitados em extremidades
- [ ] Indicador "Slide X de Y" correto

### Tema
- [ ] Tema claro funciona
- [ ] Tema escuro funciona
- [ ] Toggle tema funciona
- [ ] Tema persiste após reload

### Responsividade
- [ ] Desktop: layout 2 colunas OK
- [ ] Tablet: sidebar colapsável
- [ ] Mobile: menu hamburger funciona
- [ ] Sem scroll horizontal em nenhum tamanho
- [ ] Imagens redimensionam corretamente

### Performance
- [ ] Carregamento < 2 segundos
- [ ] Lighthouse ≥ 85 em todos critérios
- [ ] Imagens carregam sob demanda (lazy loading)

### Acessibilidade
- [ ] Navegação com TAB funciona
- [ ] ENTER submete login
- [ ] Alt text em todas imagens
- [ ] Contraste ≥ 4.5:1
- [ ] Sem erros no Console (F12)

### Conteúdo
- [ ] Todos 7 módulos têm conteúdo
- [ ] Tabelas formatadas corretamente
- [ ] Listas (bullets) formatadas
- [ ] Sem texto truncado ou overflow

---

## 🔧 TROUBLESHOOTING RÁPIDO

### ❌ Página em branco

**Solução:**
```bash
# 1. Verifique landing-page-data.json existe
ls apostila_scraped/landing-page-data.json

# 2. Abra DevTools (F12) → Console
# 3. Procure por erros vermelhos
# 4. Se faltar JSON, gere:
cd apostila_scraped
python generate_landing_page_consolidated.py
```

---

### ❌ Imagens não carregam

**Solução:**
```bash
# Verifique pasta de imagens
ls apostila_scraped/images-webp/

# Se vazia, gere otimizadas:
python run_pipeline.py
```

---

### ❌ Erros no Console (F12)

**CORS Error?**
- ✅ Normal em arquivo local
- ✅ Desaparece no GitHub Pages

**JSON Error?**
- ❌ Arquivo corrompido ou inexistente
- ✅ Execute: `python generate_landing_page_consolidated.py`

---

### ❌ Muito lento

**Causas:**
1. Internet lenta (normal)
2. JSON muito grande (897 imagens = pesado)
3. Muitas imagens carregando de uma vez

**Solução:** Aguarde carregamento completo (30-60s primeira vez)

---

## 📊 RELATÓRIO DE TESTE

**Quando todos os testes passarem, preencha:**

```markdown
## ✅ Teste Local Completo

- Data: [sua data]
- Navegador: Chrome/Firefox/Safari
- Sistema: Windows 11
- Servidor: Python http.server

### Resultados
- Login: ✅ Funcionando
- Navegação: ✅ Funcionando
- Responsividade: ✅ Funcionando
- Performance: ✅ Lighthouse 93%
- Acessibilidade: ✅ Teclado OK
- Console: ✅ Sem erros críticos

### Status
✅ PRONTO PARA DEPLOY GITHUB PAGES
```

---

## 🎯 PRÓXIMO PASSO

Quando **TODOS** os testes passarem:

1. ✅ Feche servidor local (Ctrl+C)
2. ✅ Abra: `GUIA_SINCRONIZACAO_GITHUB.md`
3. ✅ Siga os 5 passos para deploy
4. ✅ Sua landing page estará LIVE em 5 minutos! 🎉

---

**Sucesso nos testes!** 🚀
