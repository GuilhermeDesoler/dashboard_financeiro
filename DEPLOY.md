# 🚀 Deploy no Render.com

Guia completo para fazer deploy do Dashboard Financeiro no Render.com gratuitamente.

---

## 📋 Pré-requisitos

1. ✅ Conta no [Render.com](https://render.com) (gratuita)
2. ✅ Repositório Git (GitHub, GitLab ou Bitbucket)
3. ✅ Backend API já deployado e funcionando

---

## 🔧 Passo 1: Preparar o Repositório

### 1.1 Inicializar Git (se ainda não fez)

```bash
git init
git add .
git commit -m "feat: initial commit"
```

### 1.2 Criar Repositório no GitHub

1. Acesse [GitHub](https://github.com)
2. Clique em **New Repository**
3. Nome: `dashboard-financeiro`
4. Clique em **Create Repository**

### 1.3 Enviar Código para o GitHub

```bash
git remote add origin https://github.com/SEU-USUARIO/dashboard-financeiro.git
git branch -M main
git push -u origin main
```

---

## 🌐 Passo 2: Deploy no Render

### 2.1 Acessar Render Dashboard

1. Acesse [dashboard.render.com](https://dashboard.render.com)
2. Faça login ou crie uma conta (gratuita)

### 2.2 Criar Novo Web Service

1. Clique em **New +** → **Web Service**
2. Conecte seu repositório GitHub
3. Selecione `dashboard-financeiro`

### 2.3 Configurar o Service

**Preencha os campos:**

| Campo | Valor |
|-------|-------|
| **Name** | `dashboard-financeiro` (ou outro nome) |
| **Region** | `Oregon (US West)` (mais rápido) |
| **Branch** | `main` |
| **Root Directory** | (deixe vazio) |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `streamlit run src/main.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true` |
| **Instance Type** | `Free` |

### 2.4 Variáveis de Ambiente

**IMPORTANTE:** Adicione a variável de ambiente:

1. Clique em **Advanced**
2. Clique em **Add Environment Variable**
3. Adicione:

| Key | Value |
|-----|-------|
| `BASE_URL` | URL da sua API (ex: `https://sua-api.onrender.com`) |

**Exemplo:**
```
BASE_URL=https://dashboard-financeiro-api.onrender.com
```

### 2.5 Deploy

1. Clique em **Create Web Service**
2. Aguarde o build (3-5 minutos)
3. ✅ Pronto! Seu dashboard está no ar!

---

## 🔗 Acessar Aplicação

Após o deploy, você receberá uma URL:

```
https://dashboard-financeiro.onrender.com
```

O Render gera automaticamente um certificado SSL (HTTPS).

---

## ⚙️ Configurações Adicionais

### Domínio Personalizado (Opcional)

1. No Render Dashboard, clique em seu serviço
2. Vá em **Settings** → **Custom Domain**
3. Adicione seu domínio (ex: `dashboard.seusite.com`)
4. Configure DNS no seu provedor:
   ```
   CNAME @ dashboard-financeiro.onrender.com
   ```

### Auto-Deploy

Por padrão, o Render faz deploy automático quando você faz push para `main`:

```bash
git add .
git commit -m "feat: nova funcionalidade"
git push origin main
# Deploy automático é iniciado!
```

---

## 🐛 Troubleshooting

### Erro: "Application failed to start"

**Solução:**
1. Verifique os logs no Render Dashboard
2. Vá em **Logs** para ver o erro exato
3. Problemas comuns:
   - `BASE_URL` não configurada
   - Erro na `requirements.txt`
   - Python version incompatível

### Erro: "Cannot connect to API"

**Solução:**
1. Verifique se `BASE_URL` está correta
2. Certifique-se que a API está online
3. Teste a API manualmente: `curl https://sua-api.onrender.com/health`

### Build muito lento

**Solução:**
- Normal na primeira vez (3-5 min)
- Builds subsequentes são mais rápidos (cache)
- Plano Free pode ser mais lento

### App "suspende" após 15 minutos de inatividade

**Explicação:**
- Plano Free suspende após inatividade
- Primeiro acesso demora ~30s para "acordar"
- Para evitar: upgrade para plano pago

---

## 🔄 Atualizações

Para atualizar o dashboard em produção:

```bash
# 1. Faça as alterações no código
# 2. Commit e push
git add .
git commit -m "feat: minha alteração"
git push origin main

# 3. Render faz deploy automático!
```

---

## 📊 Monitoramento

### Ver Logs em Tempo Real

1. Acesse Render Dashboard
2. Clique no seu serviço
3. Clique em **Logs**
4. Veja logs em tempo real

### Métricas

No plano Free você tem:
- ✅ Banda larga ilimitada
- ✅ SSL automático
- ✅ Deploy automático
- ⚠️ 750 horas/mês
- ⚠️ Suspende após 15 min de inatividade

---

## 💰 Custos

**Plano Free:**
- ✅ $0/mês
- ✅ Perfeito para desenvolvimento e testes
- ⚠️ App suspende após inatividade

**Plano Starter ($7/mês):**
- ✅ Sem suspensão
- ✅ Mais recursos
- ✅ Melhor performance

---

## 🔒 Segurança

### Secrets (Senhas e Tokens)

**NUNCA** commite `.env` no Git!

Use variáveis de ambiente no Render:
1. Dashboard → Settings → Environment
2. Add Environment Variable
3. Exemplo: `API_KEY`, `JWT_SECRET`, etc.

### HTTPS

✅ Render fornece HTTPS automático
✅ Certificado SSL renovado automaticamente

---

## 📝 Checklist de Deploy

- [ ] Código commitado no Git
- [ ] Push para GitHub/GitLab
- [ ] Conta criada no Render
- [ ] Web Service criado
- [ ] `BASE_URL` configurada
- [ ] Build concluído com sucesso
- [ ] App acessível via URL
- [ ] Testado conexão com API
- [ ] Domínio personalizado (opcional)

---

## 🆘 Suporte

- **Render Docs:** [render.com/docs](https://render.com/docs)
- **Render Community:** [community.render.com](https://community.render.com)
- **Streamlit Docs:** [docs.streamlit.io](https://docs.streamlit.io)

---

## 🎉 Pronto!

Seu Dashboard Financeiro está no ar! 🚀

**URL de exemplo:**
```
https://dashboard-financeiro.onrender.com
```

Compartilhe com sua equipe e comece a usar!
