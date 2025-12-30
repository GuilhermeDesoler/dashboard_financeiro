# 🧪 Guia de Teste - Sistema de Autenticação e Admin

Este guia mostra como testar todas as funcionalidades implementadas no sistema de autenticação e administração.

---

## 📋 Pré-requisitos

### 1. Backend deve estar rodando

```bash
cd back_dashboard_financeiro
python src/app.py
```

Verifique se está acessível em: `http://localhost:5000`

### 2. Seed do banco deve ter sido executado

```bash
cd back_dashboard_financeiro
python scripts/seed_all.py
```

Isso cria:
- ✅ Super admin: `teste@teste.com` / senha: `123456`
- ✅ Empresa de teste
- ✅ Features do sistema

### 3. Frontend deve estar configurado

Verifique o arquivo `.env`:

```env
BASE_URL=http://localhost:5000
```

---

## 🧪 Testes do Sistema

### TESTE 1: Login com Super Admin

**Objetivo:** Verificar autenticação e redirecionamento para página Admin

**Passos:**

1. Inicie o frontend:
   ```bash
   streamlit run src/main.py
   ```

2. Acesse `http://localhost:8501`

3. **Deve aparecer a tela de login**

4. Digite as credenciais do super admin:
   - Email: `teste@teste.com`
   - Senha: `123456`

5. Clique em "🔓 Entrar"

**Resultado Esperado:**
- ✅ Mensagem de sucesso: "Bem-vindo(a), Super Admin!"
- ✅ Redirecionamento automático para página "Admin"
- ✅ Sidebar mostra nome e email do usuário
- ✅ Sidebar mostra botão "Admin" na seção Administração
- ✅ Sidebar mostra botões normais (Dashboard, Lançamentos, etc)
- ✅ Sidebar mostra botão "🚪 Sair"

---

### TESTE 2: Criar Nova Empresa

**Objetivo:** Testar criação de empresa pelo super admin

**Passos:**

1. Estando logado como super admin, vá para página "Admin" (se não estiver)

2. Clique na aba "🏭 Criar Empresa"

3. Preencha o formulário:
   - Nome da Empresa: `Empresa Teste ABC Ltda`
   - CNPJ: `12.345.678/0001-90` (opcional)
   - Telefone: `(11) 98765-4321` (opcional)
   - Plano: Selecione `premium`

4. Clique em "➕ Criar Empresa"

**Resultado Esperado:**
- ✅ Mensagem de sucesso com os dados da empresa
- ✅ Exibe o ID da empresa criada
- ✅ Formulário é limpo após criação
- ✅ Sugestão para criar usuários na aba "Criar Usuário"

---

### TESTE 3: Criar Usuário para a Empresa

**Objetivo:** Testar criação de usuário vinculado à empresa

**Passos:**

1. Na página "Admin", clique na aba "👥 Criar Usuário"

2. Preencha o formulário:
   - Empresa: Selecione `Empresa Teste ABC Ltda` (a que você acabou de criar)
   - Nome Completo: `João Silva`
   - Email: `joao@testeabc.com`
   - Senha: `senha123`
   - Super Admin: **NÃO marcar** (deixe desmarcado)

3. Clique em "➕ Criar Usuário"

**Resultado Esperado:**
- ✅ Mensagem de sucesso com dados do usuário
- ✅ Mostra nome, email, empresa e status de super admin
- ✅ Formulário é limpo após criação

---

### TESTE 4: Visualizar Empresas em Cards

**Objetivo:** Ver lista de empresas com layout de cards

**Passos:**

1. Na página "Admin", clique na aba "🏢 Empresas"

**Resultado Esperado:**
- ✅ Exibe cards das empresas cadastradas
- ✅ Cada card mostra:
  - Nome da empresa
  - CNPJ
  - Telefone
  - Plano (com cor diferente: basic=azul, premium=roxo, enterprise=laranja)
  - Status (ativa ou inativa)
  - Número de usuários
- ✅ Cor de fundo verde para empresas ativas, vermelho para inativas
- ✅ Borda esquerda na cor do plano
- ✅ Botão "🎭 Impersonate" para empresas ativas

---

### TESTE 5: Buscar Empresa

**Objetivo:** Testar filtro de busca

**Passos:**

1. Na aba "🏢 Empresas", digite no campo de busca: `ABC`

**Resultado Esperado:**
- ✅ Mostra apenas empresas que contêm "ABC" no nome
- ✅ Contador atualiza: "X empresa(s) encontrada(s)"

2. Limpe o campo de busca

**Resultado Esperado:**
- ✅ Volta a mostrar todas as empresas

---

### TESTE 6: Impersonate de Empresa

**Objetivo:** Acessar dados de uma empresa específica por 1 hora

**Passos:**

1. Na aba "🏢 Empresas", clique no botão "🎭 Impersonate" de uma empresa ativa

**Resultado Esperado:**
- ✅ Mensagem de sucesso: "Impersonando empresa: [nome]"
- ✅ Informa que token é válido por 1 hora
- ✅ Redirecionamento automático para página "Dashboard"
- ✅ Sidebar mostra aviso amarelo: "🎭 Impersonando: [nome da empresa]"
- ✅ Dashboard mostra dados DA EMPRESA impersonada (não do super admin)
- ✅ Lançamentos e modalidades são da empresa impersonada

---

### TESTE 7: Sair do Impersonate

**Objetivo:** Voltar para visão de super admin

**Passos:**

1. Enquanto em modo impersonate, role até o final da página Admin

2. Clique no botão "🔙 Sair do Impersonate"

**OU**

1. Na página Admin, role até o final

2. Deve aparecer um warning amarelo no topo: "⚠️ MODO IMPERSONATE ATIVO"

3. Clique em "🔙 Sair do Impersonate"

**Resultado Esperado:**
- ✅ Mensagem: "Modo impersonate desativado"
- ✅ Aviso amarelo no sidebar desaparece
- ✅ Token volta a ser o do super admin
- ✅ Seção Admin volta a funcionar normalmente

---

### TESTE 8: Logout

**Objetivo:** Deslogar e limpar sessão

**Passos:**

1. Em qualquer página autenticada, clique no botão "🚪 Sair" no sidebar

**Resultado Esperado:**
- ✅ Redirecionamento para tela de login
- ✅ Sidebar desaparece
- ✅ Tokens são limpos da sessão
- ✅ HTTP client não tem mais token de autenticação

---

### TESTE 9: Login com Usuário Regular

**Objetivo:** Verificar que usuário regular não vê página Admin

**Passos:**

1. Na tela de login, faça logout se estiver logado

2. Faça login com o usuário que você criou:
   - Email: `joao@testeabc.com`
   - Senha: `senha123`

**Resultado Esperado:**
- ✅ Login bem-sucedido
- ✅ Redirecionamento para página "Dashboard"
- ✅ Sidebar **NÃO** mostra seção "⚙️ Administração"
- ✅ Sidebar **NÃO** mostra botão "Admin"
- ✅ Sidebar mostra apenas: Dashboard, Lançamentos, Modalidades, Boletos
- ✅ Dashboard mostra dados DA EMPRESA do usuário
- ✅ Nome e email do usuário aparecem no sidebar

---

### TESTE 10: Persistência de Sessão

**Objetivo:** Verificar que sessão persiste durante uso (mas não após refresh)

**Passos:**

1. Faça login com qualquer usuário

2. Navegue entre as páginas (Dashboard → Lançamentos → Modalidades)

**Resultado Esperado:**
- ✅ Token permanece válido
- ✅ Não pede login novamente
- ✅ Dados carregam corretamente

3. **Dê refresh na página (F5 ou Ctrl+R)**

**Resultado Esperado:**
- ✅ Session state é limpo (comportamento normal do Streamlit)
- ✅ Volta para tela de login
- ⚠️ **ISSO É NORMAL:** Streamlit não persiste session_state no navegador

**Nota:** Para persistência entre refreshes, seria necessário usar cookies ou localStorage (fora do escopo do Streamlit padrão).

---

### TESTE 11: Credenciais Inválidas

**Objetivo:** Testar tratamento de erros de autenticação

**Passos:**

1. Na tela de login, digite:
   - Email: `usuario@invalido.com`
   - Senha: `senhaerrada`

2. Clique em "🔓 Entrar"

**Resultado Esperado:**
- ✅ Mensagem de erro: "❌ Email ou senha incorretos"
- ✅ Não redireciona
- ✅ Permanece na tela de login

---

### TESTE 12: Campos Vazios

**Objetivo:** Validação de formulários

**Testes em Login:**

1. Deixe email e senha vazios
2. Clique em "🔓 Entrar"

**Resultado Esperado:**
- ✅ Erro: "⚠️ Por favor, preencha email e senha"

**Testes em Criar Empresa:**

1. Vá para Admin → Criar Empresa
2. Deixe nome da empresa vazio
3. Clique em "➕ Criar Empresa"

**Resultado Esperado:**
- ✅ Erro: "⚠️ Por favor, preencha o nome da empresa"

**Testes em Criar Usuário:**

1. Vá para Admin → Criar Usuário
2. Deixe algum campo obrigatório vazio
3. Clique em "➕ Criar Usuário"

**Resultado Esperado:**
- ✅ Erro: "⚠️ Por favor, preencha todos os campos obrigatórios"

4. Preencha tudo mas use senha com menos de 6 caracteres

**Resultado Esperado:**
- ✅ Erro: "⚠️ A senha deve ter no mínimo 6 caracteres"

---

### TESTE 13: Duplicação de Email

**Objetivo:** Verificar que sistema previne emails duplicados

**Passos:**

1. Tente criar um usuário com email `joao@testeabc.com` (que já existe)

**Resultado Esperado:**
- ✅ Erro: "❌ Email já cadastrado no sistema"

---

### TESTE 14: Acesso Direto sem Autenticação

**Objetivo:** Verificar que middleware bloqueia acesso não autenticado

**Passos:**

1. Faça logout (ou abra aba anônima)

2. Tente manipular session_state diretamente no console do navegador (não é possível em Streamlit)

**Resultado Esperado:**
- ✅ Sempre redireciona para Login se não houver `is_authenticated = True`

---

## 🎯 Checklist Final

Após todos os testes, verifique:

- [ ] ✅ Login funciona para super admin
- [ ] ✅ Login funciona para usuário regular
- [ ] ✅ Super admin vê página Admin
- [ ] ✅ Usuário regular NÃO vê página Admin
- [ ] ✅ Criar empresa funciona
- [ ] ✅ Criar usuário funciona
- [ ] ✅ Empresas aparecem em cards
- [ ] ✅ Busca de empresas funciona
- [ ] ✅ Impersonate funciona (token de 1h)
- [ ] ✅ Sair do impersonate funciona
- [ ] ✅ Logout limpa sessão
- [ ] ✅ Validações de formulário funcionam
- [ ] ✅ Erros de autenticação são tratados
- [ ] ✅ Sidebar mostra informações corretas
- [ ] ✅ Token é injetado no HTTP client
- [ ] ✅ Navegação entre páginas funciona

---

## 🐛 Problemas Conhecidos

### Session State não persiste após refresh

**Comportamento:** Ao dar F5 na página, o usuário é deslogado.

**Causa:** Streamlit limpa o `session_state` ao recarregar a página.

**Solução (futuro):**
- Implementar persistência com cookies
- Usar `streamlit-cookies-manager` ou similar
- Armazenar token em localStorage via JavaScript

### Token expira após 24 horas

**Comportamento:** Após 24 horas, o access token expira.

**Solução atual:** Usuário precisa fazer login novamente.

**Solução futura:** Implementar refresh automático usando o refresh_token (válido por 7 dias).

---

## 📊 Fluxo Visual do Sistema

```
┌─────────────┐
│   INÍCIO    │
└──────┬──────┘
       │
       v
┌─────────────────┐
│  Tela de Login  │
└──────┬──────────┘
       │
       │ Login bem-sucedido
       v
  ┌─────────────┐
  │ É Super     │
  │ Admin?      │
  └─┬─────────┬─┘
    │         │
   SIM       NÃO
    │         │
    v         v
┌────────┐  ┌──────────┐
│ Admin  │  │Dashboard │
│ Page   │  │   Page   │
└────┬───┘  └────┬─────┘
     │           │
     │ Impersonate
     └─────┬─────┘
           │
           v
    ┌──────────────┐
    │  Dashboard   │
    │ da Empresa   │
    │ (1 hora)     │
    └──────────────┘
```

---

## 🔒 Segurança Implementada

- ✅ Senhas hasheadas no backend (bcrypt)
- ✅ JWT tokens com expiração (24h access, 7d refresh)
- ✅ Tokens assinados (não podem ser alterados)
- ✅ Middleware de autenticação em todas as páginas
- ✅ Verificação de `is_super_admin` para rotas admin
- ✅ Impersonate com token limitado (1 hora)
- ✅ Logs de auditoria no backend (todas ações críticas)
- ✅ Isolamento multi-tenant (cada empresa tem seu banco)
- ✅ Token enviado via Authorization header (Bearer)

---

## 📝 Próximos Passos (Melhorias Futuras)

1. **Persistência de Login:**
   - Adicionar `streamlit-cookies-manager`
   - Armazenar refresh_token em cookie seguro
   - Auto-refresh do access_token quando expirar

2. **Página de Usuários:**
   - Visualizar usuários da empresa
   - Editar/desativar usuários
   - Atribuir roles e permissões

3. **Dashboard Admin:**
   - Estatísticas do sistema
   - Gráficos de uso por empresa
   - Logs de auditoria visualizados

4. **Recuperação de Senha:**
   - Endpoint "Esqueci minha senha"
   - Envio de email com token de reset
   - Página de redefinição de senha

5. **Edição de Empresas:**
   - Atualizar dados da empresa
   - Desativar empresa
   - Alterar plano

---

✅ **Sistema de Autenticação e Admin Completo!**

Implementado seguindo Clean Architecture e totalmente integrado com o backend existente.
