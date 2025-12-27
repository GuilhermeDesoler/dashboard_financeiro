# Dashboard Financeiro

Dashboard financeiro desenvolvido com Streamlit seguindo os princípios de Clean Architecture.

## Arquitetura

O projeto segue a Clean Architecture com as seguintes camadas:

```
src/
├── domain/              # Camada de Domínio (Regras de Negócio)
│   ├── entities/        # Entidades de domínio
│   └── repositories/    # Interfaces dos repositórios
├── application/         # Camada de Aplicação (Casos de Uso)
│   └── use_cases/       # Casos de uso da aplicação
├── infrastructure/      # Camada de Infraestrutura (Detalhes Externos)
│   ├── api/             # Implementação dos repositórios (API)
│   └── http/            # Cliente HTTP
├── presentation/        # Camada de Apresentação (UI)
│   └── components/      # Componentes reutilizáveis
├── views/               # Views do Streamlit
├── config/              # Configurações e variáveis de ambiente
├── dependencies.py      # Injeção de dependências
└── main.py             # Ponto de entrada da aplicação
```

## Funcionalidades

- **Dashboard**: Visualização de métricas e gráficos financeiros
- **Lançamentos**: Gerenciamento de lançamentos financeiros
- **Modalidades**: CRUD completo de modalidades de pagamento
- **Boletos**: Gestão de boletos

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
   BASE_URL=http://localhost:8000
   ```

## Executar

```bash
streamlit run src/main.py
```

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

## Tecnologias

- **Streamlit**: Framework web para Python
- **Pandas**: Manipulação e análise de dados
- **Requests**: Cliente HTTP para consumir APIs
- **Clean Architecture**: Organização do código em camadas

## Estrutura de Dados

### PaymentModality (Modalidade de Pagamento)
- `id`: Identificador único
- `name`: Nome da modalidade
- `is_active`: Status ativo/inativo
- `created_at`: Data de criação
- `updated_at`: Data de atualização

### FinancialEntry (Lançamento Financeiro)
- `id`: Identificador único
- `value`: Valor do lançamento
- `date`: Data do lançamento
- `modality_id`: ID da modalidade de pagamento
- `modality_name`: Nome da modalidade
- `created_at`: Data de criação
- `updated_at`: Data de atualização

## API Endpoints

### Modalidades de Pagamento
- `GET /api/payment-modalities` - Listar todas
- `POST /api/payment-modalities` - Criar nova
- `PUT /api/payment-modalities/<id>` - Atualizar
- `DELETE /api/payment-modalities/<id>` - Excluir
- `PATCH /api/payment-modalities/<id>/toggle` - Ativar/Desativar

### Lançamentos Financeiros
- `GET /api/financial-entries` - Listar todos (com filtros opcionais)
- `POST /api/financial-entries` - Criar novo
- `PUT /api/financial-entries/<id>` - Atualizar
- `DELETE /api/financial-entries/<id>` - Excluir

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
