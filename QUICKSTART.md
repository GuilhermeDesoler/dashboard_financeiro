# ⚡ Quick Start - Deploy no Render

Guia super rápido para colocar seu dashboard no ar em 5 minutos!

---

## 🚀 Método 1: Deploy Automático (Mais Rápido)

### 1️⃣ Preparar Git

```bash
# Se ainda não inicializou o Git
git init
git add .
git commit -m "feat: initial commit"

# Criar repositório no GitHub e fazer push
git remote add origin https://github.com/SEU-USUARIO/dashboard-financeiro.git
git branch -M main
git push -u origin main
```

### 2️⃣ Deploy no Render

1. Acesse: https://dashboard.render.com
2. Clique **New +** → **Web Service**
3. Conecte GitHub e selecione o repositório
4. **Configure:**
   - **Name:** `dashboard-financeiro`
   - **Start Command:** `streamlit run src/main.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true`
   - **Instance Type:** Free

5. **Adicione variável de ambiente:**
   - **Key:** `BASE_URL`
   - **Value:** `https://sua-api.onrender.com`

6. Clique **Create Web Service**

### 3️⃣ Pronto! 🎉

Aguarde 3-5 minutos e acesse: `https://dashboard-financeiro.onrender.com`

---

## 📋 Checklist Rápido

- [ ] Código no GitHub
- [ ] Conta no Render criada
- [ ] Web Service criado
- [ ] Variável `BASE_URL` configurada
- [ ] Build completo
- [ ] App acessível

---

## 🔧 Comandos Úteis

### Atualizar App em Produção

```bash
git add .
git commit -m "feat: nova funcionalidade"
git push origin main
# Deploy automático!
```

### Testar Localmente Antes

```bash
streamlit run src/main.py
```

---

## 🐛 Problema?

**App não inicia?**
- Verifique logs no Render Dashboard → Logs
- Certifique-se que `BASE_URL` está configurada

**API não conecta?**
- Teste: `curl https://sua-api.onrender.com/health`
- Verifique se API está online

**App lento?**
- Primeira requisição demora ~30s (plano Free)
- App "acorda" após inatividade

---

## 📖 Documentação Completa

Ver **[DEPLOY.md](DEPLOY.md)** para guia detalhado.

---

## 💡 Dicas

✅ **URL customizada:** Configure domínio próprio no Render
✅ **Auto-deploy:** Push para `main` = deploy automático
✅ **Logs:** Monitore erros em tempo real no Dashboard
✅ **Grátis:** 750 horas/mês no plano Free

---

**Pronto para deploy?** Vamos lá! 🚀
