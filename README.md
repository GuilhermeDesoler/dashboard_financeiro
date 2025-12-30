# 💰 Dashboard Financeiro

Dashboard financeiro multi-tenant desenvolvido com Streamlit seguindo os princípios de Clean Architecture.

Sistema completo com autenticação, controle de acesso, administração de empresas e usuários, e modo impersonate.

## ✨ Funcionalidades

### 🔐 Sistema de Autenticação
- Login seguro com JWT tokens
- Persistência de sessão durante uso
- Controle de acesso baseado em roles (RBAC)
- Logout com limpeza completa de sessão

### ⚙️ Painel Administrativo (Super Admin)
- **Gestão de Empresas:**
  - Visualização em cards com informações completas
  - Criação de novas empresas
  - Filtro e busca por nome/CNPJ
  - Suporte a múltiplos planos (Basic, Premium, Enterprise)

- **Gestão de Usuários:**
  - Criação de usuários vinculados a empresas
  - Atribuição de permissões de super admin
  - Validação de emails únicos

- **Modo Impersonate (1 hora):**
  - Acesse dados de qualquer empresa
  - Veja exatamente o que o cliente vê
  - Ideal para suporte técnico
  - Registrado em logs de auditoria

### 📊 Dashboards Operacionais
- **Dashboard**: Visualização de métricas e gráficos financeiros
- **Lançamentos**: Gerenciamento de lançamentos financeiros
- **Modalidades**: CRUD completo de modalidades de pagamento
- **Boletos**: Gestão de boletos

### 🏢 Multi-Tenancy
- Isolamento total de dados por empresa
- Cada empresa tem seu próprio banco de dados
- Impossível vazar dados entre empresas

## 🏗 Arquitetura

O projeto segue a Clean Architecture com as seguintes camadas:

```
src/
├── domain/              # Camada de Domínio (Regras de Negócio)
│   ├── entities/        # User, Company, Auth, PaymentModality, FinancialEntry
│   └── repositories/    # Interfaces dos repositórios
├── application/         # Camada de Aplicação (Casos de Uso)
│   └── use_cases/       # Auth, Admin, PaymentModality, FinancialEntry
├── infrastructure/      # Camada de Infraestrutura (Detalhes Externos)
│   ├── api/             # Implementação dos repositórios (API REST)
│   └── http/            # Cliente HTTP com autenticação
├── presentation/        # Camada de Apresentação (UI)
│   └── components/      # Componentes reutilizáveis
├── views/               # Views do Streamlit (Login, Admin, Dashboard, etc)
├── config/              # Configurações e variáveis de ambiente
├── dependencies.py      # Injeção de dependências (Container)
└── main.py             # Middleware de autenticação e roteamento
```

## Instalação

1. Clone o repositório
2. Crie um ambiente virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate     # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente:
   ```bash
   cp .env.example .env
   ```
   Edite o arquivo `.env` e configure a URL da API:
   ```
   BASE_URL=http://localhost:5000
   ```

5. **Certifique-se que o backend está rodando:**

   Veja a documentação completa do backend em `back_dashboard_financeiro/README.md`

   Quick start do backend:
   ```bash
   cd back_dashboard_financeiro
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   python scripts/seed_all.py  # Cria super admin
   python src/app.py
   ```

## 🚀 Executar

```bash
streamlit run src/main.py
```

Acesse: `http://localhost:8501`

**Login padrão (super admin):**
- Email: `teste@teste.com`
- Senha: `123456`

## Deploy em Produção

### Render.com (Recomendado - Gratuito)

Siga o guia completo em **[DEPLOY.md](DEPLOY.md)** para fazer deploy no Render.com.

**Resumo rápido:**
1. Push do código para GitHub
2. Crie Web Service no Render
3. Configure variável `BASE_URL`
4. Deploy automático!

Sua aplicação estará online em minutos: `https://seu-app.onrender.com`

## Personalização de Tema

O projeto vem com um tema dark green configurado. Para personalizar:

1. Edite o arquivo `.streamlit/config.toml`
2. Veja 10+ temas prontos em `.streamlit/themes.md`
3. Copie e cole o tema desejado
4. Reinicie o Streamlit

**Tema padrão:**
- Verde vibrante (#00C853)
- Fundo escuro (#0E1117)
- Perfeito para dashboards financeiros

## 🛠 Tecnologias

### Frontend
- **Streamlit 1.30.0+** - Framework web para Python
- **Pandas** - Manipulação e análise de dados
- **Plotly** - Gráficos interativos
- **Requests** - Cliente HTTP para consumir APIs

### Backend (Integrado)
- **Flask** - Framework web
- **MongoDB** - Banco de dados NoSQL multi-tenant
- **PyJWT** - Autenticação JWT
- **bcrypt** - Hash de senhas

### Arquitetura
- **Clean Architecture** - Organização do código em camadas
- **SOLID** - Princípios de design
- **Dependency Injection** - Inversão de controle
- **Repository Pattern** - Abstração de persistência

## 📖 Documentação Completa

- **[IMPLEMENTACAO_COMPLETA.md](IMPLEMENTACAO_COMPLETA.md)** - Documentação técnica completa da implementação
- **[GUIA_TESTE_AUTENTICACAO.md](GUIA_TESTE_AUTENTICACAO.md)** - Guia passo a passo para testar todas as funcionalidades
- **[DEPLOY.md](DEPLOY.md)** - Instruções de deploy em produção

## 🧪 Testes

Para testar o sistema completo, siga o guia em: **[GUIA_TESTE_AUTENTICACAO.md](GUIA_TESTE_AUTENTICACAO.md)**

**Quick tests:**

1. **Login como super admin:**
   - Email: `teste@teste.com` / Senha: `123456`
   - Deve redirecionar para página Admin

2. **Criar empresa:**
   - Admin → Criar Empresa → Preencher formulário
   - Deve criar e mostrar ID

3. **Criar usuário:**
   - Admin → Criar Usuário → Selecionar empresa
   - Deve criar com sucesso

4. **Impersonate:**
   - Admin → Empresas → Clicar "Impersonate"
   - Deve acessar Dashboard da empresa (1 hora)

5. **Logout:**
   - Sidebar → Sair
   - Deve limpar sessão e voltar ao login

## 🔐 Segurança

- ✅ Autenticação JWT (24h) + Refresh Token (7 dias)
- ✅ Senhas hasheadas com bcrypt no backend
- ✅ RBAC (Role-Based Access Control)
- ✅ Multi-tenancy com isolamento de dados
- ✅ Tokens assinados (impossível falsificar)
- ✅ Impersonate limitado a 1 hora
- ✅ Logs de auditoria de todas ações críticas
- ✅ Middleware de autenticação em todas as rotas

## 🎯 Níveis de Acesso

### 1. Não Autenticado
- Acessa apenas: Tela de Login

### 2. Usuário Regular
- Páginas: Dashboard, Lançamentos, Modalidades, Boletos
- Vê apenas dados da própria empresa
- Token JWT válido por 24 horas

### 3. Super Admin
- Páginas: TODAS (Admin + páginas regulares)
- Pode criar empresas e usuários
- Pode fazer impersonate de qualquer empresa
- Ações críticas registradas em log

### 4. Super Admin (Modo Impersonate)
- Vê dados APENAS da empresa impersonada
- NÃO vê página Admin (previne ações acidentais)
- Token válido por 1 hora
- Aviso visual permanente no sidebar

## 📊 Estrutura de Dados

### User (Usuário)
- `id`: UUID
- `email`: Email único
- `name`: Nome completo
- `company_id`: UUID da empresa
- `is_super_admin`: Boolean
- `is_active`: Boolean
- `role_ids`: Lista de roles
- `features`: Lista de permissões

### Company (Empresa)
- `id`: UUID
- `name`: Nome da empresa
- `cnpj`: CNPJ (opcional)
- `phone`: Telefone (opcional)
- `plan`: basic | premium | enterprise
- `is_active`: Boolean
- `users_count`: Número de usuários

### PaymentModality (Modalidade de Pagamento)
- `id`: UUID
- `name`: Nome da modalidade
- `color`: Cor em hexadecimal
- `is_active`: Boolean

### FinancialEntry (Lançamento Financeiro)
- `id`: UUID
- `value`: Valor decimal
- `date`: Data do lançamento
- `modality_id`: UUID da modalidade
- `modality_name`: Nome da modalidade
- `modality_color`: Cor da modalidade

## 🔌 API Endpoints Utilizados

### Autenticação
- `POST /api/auth/login` - Login
- `POST /api/auth/refresh` - Refresh token
- `GET /api/auth/me` - Dados do usuário atual

### Admin - Empresas
- `GET /api/admin/companies` - Listar empresas
- `GET /api/admin/companies/{id}` - Detalhes da empresa
- `POST /api/admin/companies` - Criar empresa
- `POST /api/admin/impersonate/{company_id}` - Impersonate (1h)

### Admin - Usuários
- `GET /api/admin/users` - Listar usuários
- `POST /api/admin/users` - Criar usuário

### Modalidades de Pagamento
- `GET /api/payment-modalities` - Listar todas
- `POST /api/payment-modalities` - Criar nova
- `PUT /api/payment-modalities/{id}` - Atualizar
- `DELETE /api/payment-modalities/{id}` - Excluir
- `PATCH /api/payment-modalities/{id}/toggle` - Ativar/Desativar

### Lançamentos Financeiros
- `GET /api/financial-entries` - Listar todos (com filtros)
- `POST /api/financial-entries` - Criar novo
- `PUT /api/financial-entries/{id}` - Atualizar
- `DELETE /api/financial-entries/{id}` - Excluir

## Desenvolvimento

O projeto utiliza Clean Architecture para manter o código organizado e testável:

- **Domain**: Contém as regras de negócio e entidades
- **Application**: Casos de uso que orquestram o fluxo de dados
- **Infrastructure**: Implementações concretas (API, banco de dados, etc)
- **Presentation**: Interface com o usuário (Views Streamlit)

Esta separação permite:
- Facilidade para testes
- Independência de frameworks
- Flexibilidade para mudanças
- Código mais limpo e manutenível
