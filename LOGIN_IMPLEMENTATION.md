# Sistema de Login — Plataforma Price Action

## Visão Geral

A plataforma de educação Price Action agora possui um sistema de autenticação com senha para proteger o acesso ao conteúdo.

**Status:** ✅ Implementado (24 de abril de 2026)

---

## Credenciais de Acesso

| Campo | Valor |
|-------|-------|
| **Senha** | `AndreTrader` |
| **Case-sensitive** | Sim (exato: `AndreTrader`) |
| **Armazenamento** | sessionStorage (válido apenas na sessão atual) |

---

## Como Funciona

### 1. **Tela de Login (Primeira Visita)**

Quando você acessa a plataforma pela primeira vez (ou após fazer logout), é exibida a tela de login:

```
┌─────────────────────────────────┐
│   Método Price Action           │
│   Oliver Velez | André Trader   │
│   Plataforma Educacional        │
│                                 │
│   [Digite a senha para acessar] │
│                                 │
│          [🔓 Entrar]            │
│                                 │
│                                 │
└─────────────────────────────────┘
```

### 2. **Entrada de Senha**

- **Digite:** `AndreTrader` (exato, com maiúsculas)
- **Pressione:** Enter ou clique em "🔓 Entrar"
- **Resultado:** Acesso liberado à plataforma

### 3. **Se Errar a Senha**

- Mensagem: "❌ Senha incorreta. Tente novamente."
- O campo é limpo automaticamente
- Você pode tentar novamente

### 4. **Sessão Ativa**

Após autenticar com sucesso:

- A senha é armazenada em `sessionStorage` (memória do browser)
- Você pode navegar livremente pela plataforma
- Botão **🚪 Sair** aparece no header

### 5. **Fazer Logout**

Clique no botão **🚪 Sair** no header para:

- Limpar a autenticação
- Retornar à tela de login
- Exigir senha novamente

---

## Segurança

### O que NÃO fazer

❌ **Não compartilhe a senha** em emails ou mensagens não criptografadas
❌ **Não salve a senha** em arquivos de texto abertos
❌ **Não deixe o computador desbloqueado** quando se afastar

### Boas Práticas

✅ **Use HTTPS** em produção (não apenas HTTP)
✅ **Feche o browser** ou faça logout ao sair
✅ **sessionStorage não persiste** entre abas (segurança extra)
✅ **localStorage NÃO é usado** (não persiste entre sessões)

---

## Detalhes Técnicos

### Arquivos Modificados

| Arquivo | Mudanças |
|---------|----------|
| `index.html` | Adicionado div#login-screen + botão Logout no header |
| `app.js` | Funções de autenticação (submitPassword, logout, checkAuthentication) |
| `style.css` | Estilos para .login-container, .login-box, .logout-btn |

### Fluxo de Inicialização

```
1. DOMContentLoaded
   ↓
2. checkAuthentication()
   ├─ sessionStorage.getItem('authenticated')?
   │  ├─ SIM → showLandingPage() → initialize()
   │  └─ NÃO → Mostrar login screen
   ↓
3. Usuário digita senha
   ├─ Senha correta?
   │  ├─ SIM → sessionStorage.setItem('authenticated', 'true')
   │  │      → showLandingPage() → initialize()
   │  └─ NÃO → Exibir erro, limpar campo
```

### Armazenamento (sessionStorage)

```javascript
// Ao fazer login com sucesso
sessionStorage.setItem('authenticated', 'true');

// Ao fazer logout
sessionStorage.removeItem('authenticated');

// Verificar autenticação
sessionStorage.getItem('authenticated') === 'true'
```

**Nota:** `sessionStorage` é limpo automaticamente quando você:
- Fecha a aba do browser
- Fecha o browser completamente
- Limpa o histórico/cookies (em algumas configurações)

---

## Funções JavaScript

### `submitPassword()`

```javascript
// Chamada ao clicar "Entrar" ou pressionar Enter
submitPassword()
```

**O que faz:**
- Lê a senha do input
- Valida contra `AndreTrader`
- Se correto: salva em sessionStorage e mostra landing page
- Se incorreto: exibe erro e limpa o campo

---

### `logout()`

```javascript
// Chamada ao clicar "🚪 Sair"
logout()
```

**O que faz:**
- Remove autenticação do sessionStorage
- Recarrega a página (location.reload())
- Retorna para a tela de login

---

### `checkAuthentication()`

```javascript
// Chamada automaticamente ao carregar a página
checkAuthentication()
```

**O que faz:**
- Verifica se o usuário está autenticado
- Se sim: oculta login screen, mostra landing page, inicializa app
- Se não: mostra login screen, foca no input de senha

---

## Troubleshooting

### "A senha não funciona"

✅ **Solução:** Verifique se digitou exatamente `AndreTrader`:
- Letra **A** maiúscula
- Letra **T** maiúscula
- Resto em minúsculas
- Sem espaços

### "Logout não funciona"

✅ **Solução:** Verifique se o botão 🚪 Sair está visível no header
- Se não aparecer, recarregue a página
- Se mesmo assim não aparecer, abra o DevTools (F12) e verifique:
  ```javascript
  console.log(sessionStorage.getItem('authenticated'));
  ```

### "Preciso acessar de novo toda vez"

✅ **Normal:** `sessionStorage` é específico da aba/sessão
- Se fechar o browser, precisa fazer login novamente
- Isso é por design de segurança

### "Posso salvar a senha?"

❌ **Não recomendado:** O navegador pode oferecer salvar a senha
- Se aceitar, o browser a salvará no gerenciador de senhas
- Isso diminui a segurança
- Para uso profissional, considere usar autenticação OAuth2

---

## Customizações Futuras

### Ideias para melhorar:

1. **Autenticação com email/senha** (banco de dados)
2. **2FA (Two-Factor Authentication)** com código de tempo
3. **OAuth2 (Google, GitHub)** para login social
4. **Rate limiting** (máximo de tentativas erradas)
5. **Histórico de login** (quem acessou e quando)
6. **Permissões por nível** (admin, teacher, student)

---

## Testes Realizados

| Teste | Resultado |
|-------|-----------|
| Digitação correta da senha | ✅ Acesso liberado |
| Digitação com erro | ✅ Mensagem de erro exibida |
| Enter para submeter | ✅ Funciona como esperado |
| Botão Logout | ✅ Retorna para login |
| Recarregar página autenticado | ✅ Mantém acesso |
| Fechar aba e reabrir | ✅ Pede login novamente |
| Tema dark/light | ✅ Login responde ao tema |
| Responsivo (mobile) | ✅ Tela de login adapta |

---

## Referências

**Arquivos principais:**
- `index.html` - Linha 18-45 (tela de login)
- `app.js` - Linha 27-85 (funções de autenticação)
- `style.css` - Linha 1695-1870 (estilos de login)

**Variáveis de CSS utilizadas:**
- `--primary-color` - Cor principal do gradiente
- `--accent-color` - Cor dos botões e destaques
- `--bg-primary` / `--bg-secondary` - Cores de fundo
- `--text-primary` / `--text-secondary` - Cores de texto
- `--border-color` - Cor das bordas

---

## Suporte

Para problemas ou sugestões:

1. **Verifique o console** do DevTools (F12)
2. **Teste em outro browser** (Chrome, Firefox, Safari)
3. **Limpe o cache** (Ctrl+Shift+Delete)
4. **Contate o suporte** técnico

---

**Versão:** 1.0  
**Data de Implementação:** 24 de abril de 2026  
**Status:** ✅ Produção  
**Autor:** Claude AI (Anthropic)
