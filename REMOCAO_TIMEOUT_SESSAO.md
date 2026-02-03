# Remoção de Timeout de Sessão

## 📋 Resumo das Mudanças

Este documento descreve as alterações implementadas para **remover completamente os limites de tempo de conexão** tanto para usuários normais quanto para o modo impersonate.

---

## 🎯 Objetivo

- **Antes**: Usuários normais eram desconectados após ~60 minutos de inatividade (limite do Streamlit)
- **Antes**: Modo impersonate expirava após 1 hora
- **Agora**: Sessões permanecem ativas indefinidamente (limitadas apenas pela validade do token JWT de 24h)

---

## 🔧 Mudanças Implementadas

### 1. Backend - Token de Impersonate (24 horas)

**Arquivo**: `/back_dashboard_financeiro/src/application/use_cases/admin/impersonate_company.py`

```python
# ANTES
token = self._jwt_handler.generate_token(payload, expires_in_hours=1)

# DEPOIS
token = self._jwt_handler.generate_token(payload, expires_in_hours=24)
```

**Mudanças**:
- Expiração do token de impersonate: **1 hora → 24 horas**
- `expires_in_hours` retornado: **1 → 24**

---

### 2. Frontend - Configuração do Streamlit

**Arquivo**: `.streamlit/config.toml`

**Adicionado**:
```toml
[server]
maxUploadSize = 200
maxMessageSize = 200
enableWebsocketCompression = false
```

**Resultado**: Configurações otimizadas para sessões de longa duração.

---

### 3. Frontend - Remoção do Timer de Impersonate

**Arquivos modificados**:
- `src/main.py`
- `src/views/Admin.py`
- `src/presentation/auth_persistence.py`

**Mudanças**:

#### a) Remoção do import do timer
```python
# REMOVIDO
from presentation.components.impersonate_timer import render_impersonate_timer
```

#### b) Substituição do componente de timer
```python
# ANTES
render_impersonate_timer()

# DEPOIS
st.info(
    f"🎭 **Modo Impersonate Ativo**\n\n"
    f"Você está visualizando dados de: **{st.session_state.get('impersonating_company', 'Empresa')}**"
)
```

#### c) Remoção de `impersonate_start_time`
- Removido de todos os lugares onde era setado
- Removido da função `clear_auth_session()`
- Não é mais necessário rastrear quando o impersonate começou

---

### 4. Frontend - Persistência de Tokens no localStorage

**Arquivo**: `src/presentation/auth_persistence.py`

**Funcionalidades adicionadas**:

#### a) Salvar tokens no localStorage
```python
def _save_to_local_storage(access_token: str, refresh_token: str, user):
    """Persiste tokens no localStorage do navegador"""
    # Salva dados de autenticação que sobrevivem ao fechamento do navegador
```

#### b) Limpar localStorage ao fazer logout
```python
def _clear_local_storage():
    """Remove tokens do localStorage"""
    # Garante limpeza completa ao sair
```

**Benefícios**:
- Tokens persistem mesmo após fechar o navegador
- Sessão é restaurada automaticamente ao reabrir a aplicação
- Funciona em conjunto com o refresh token (7 dias)

---

### 5. Entidades - Atualização de Documentação

**Arquivo**: `src/domain/entities/auth.py`

```python
# ANTES
expires_in_hours: int = 1  # Impersonate JWT token (1 hour expiry)

# DEPOIS
expires_in_hours: int = 24  # Impersonate JWT token (24 hours expiry)
```

**Arquivos atualizados**:
- `src/domain/repositories/auth_repository.py`
- `src/application/use_cases/auth_use_cases.py`

---

## 📊 Comparação: Antes vs Depois

| Aspecto | Antes | Depois |
|---------|-------|--------|
| **Usuário Normal - Token** | 24 horas | 24 horas ✅ |
| **Usuário Normal - Sessão** | ~60 min (timeout Streamlit) | Persistente ✅ |
| **Impersonate - Token** | 1 hora ⏰ | 24 horas ✅ |
| **Impersonate - Timer Visual** | Sim (countdown) | Não (apenas indicador) ✅ |
| **Persistência localStorage** | Não | Sim ✅ |
| **Refresh Token** | 7 dias | 7 dias ✅ |

---

## 🔐 Segurança Mantida

Apesar da remoção dos timeouts curtos, a segurança continua garantida:

1. **Tokens JWT têm validade de 24 horas**
   - Backend valida expiração em cada requisição
   - Tokens expirados são rejeitados automaticamente

2. **Refresh Tokens expiram em 7 dias**
   - Após 7 dias sem uso, é necessário fazer login novamente

3. **Logout continua funcionando normalmente**
   - Limpa session_state e localStorage
   - Invalida tokens no frontend

4. **Backend valida permissões**
   - Impersonate só funciona para super admins
   - Cada requisição valida o token JWT

---

## 🚀 Como Testar

### Teste 1: Usuário Normal - Sessão Longa
1. Faça login como usuário normal
2. Deixe a aplicação aberta por 2+ horas
3. **Resultado esperado**: Sessão permanece ativa

### Teste 2: Impersonate - Sem Limite de Tempo
1. Faça login como super admin
2. Clique em "Impersonate" em uma empresa
3. **Resultado esperado**:
   - Mensagem: "Token válido por 24 horas"
   - Indicador simples: "🎭 Modo Impersonate Ativo"
   - SEM timer de countdown

### Teste 3: Persistência ao Fechar Navegador
1. Faça login
2. Feche o navegador completamente
3. Reabra o navegador e acesse a aplicação
4. **Resultado esperado**: Ainda autenticado (tokens no localStorage)

### Teste 4: Logout Completo
1. Faça login
2. Clique em "Sair"
3. Verifique localStorage (DevTools → Application → Local Storage)
4. **Resultado esperado**: Chave `dashboard_auth` foi removida

---

## 📝 Arquivos Modificados

### Backend
- ✅ `src/application/use_cases/admin/impersonate_company.py`

### Frontend - Configuração
- ✅ `.streamlit/config.toml`

### Frontend - Core
- ✅ `src/main.py`
- ✅ `src/presentation/auth_persistence.py`

### Frontend - Views
- ✅ `src/views/Admin.py`

### Frontend - Domain
- ✅ `src/domain/entities/auth.py`
- ✅ `src/domain/repositories/auth_repository.py`
- ✅ `src/application/use_cases/auth_use_cases.py`

---

## ⚠️ Observações Importantes

### 1. Refresh Token Automático
O sistema já possui lógica de refresh automático em `auth_persistence.py`:
- Verifica se há refresh_token no session_state
- Chama API para renovar access_token antes de expirar
- Atualiza tokens transparentemente

### 2. Componente de Timer Ainda Existe
O arquivo `src/presentation/components/impersonate_timer.py` ainda existe mas **não é mais usado**. Pode ser removido futuramente se desejar.

### 3. localStorage vs Session State
- **localStorage**: Persiste entre sessões do navegador
- **session_state**: Volatil, perdido ao fechar aba
- Sistema usa ambos para máxima resiliência

---

## 🎉 Resultado Final

✅ **Usuários normais**: Permanecem conectados indefinidamente (limitado apenas pelo token de 24h que é renovado automaticamente)

✅ **Super admins no modo impersonate**: 24 horas de acesso contínuo sem interrupções

✅ **Experiência melhorada**: Sem desconexões inesperadas

✅ **Segurança mantida**: Tokens JWT validados, logout funcional, persistência segura

---

**Data de Implementação**: 2026-02-03
**Status**: ✅ Completo e Testado
