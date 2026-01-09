# Implementações Pendentes - Frontend

## Backend Completo ✅

- Campo `paid` no modelo Account
- Campo `entry_type` no FinancialEntry
- Campo `interest_rate` no BankLimit
- Rota PATCH para atualizar accounts

## Frontend - A Implementar

### 1. Atualizar Entidades Frontend

#### `/src/domain/entities/account.py`
- Adicionar campo `paid: bool = False`

#### `/src/domain/entities/bank_limit.py`
- Adicionar campo `interest_rate: float = 0.0`

#### `/src/domain/entities/financial_entry.py`
- Adicionar campo `entry_type: str = "normal"`

### 2. Dashboard (`/src/views/Dashboard.py`)

**Adicionar 2 cards no topo:**
- Card 1: Total geral do período
- Card 2: Total removendo lançamentos do tipo "crediário"

**Localização:** Antes dos cards de modalidades (linha ~73)

### 3. Ticket/Boletos (`/src/views/Ticket.py`)

**Modificações completas:**
- Implementar tabela estilo Expenses com colunas:
  - Data
  - Valor
  - Descrição
  - Checkbox "Pago" (salva boolean no backend)
- Cor vermelha para não pagos, verde para pagos
- Adicionar cards mostrando valores a pagar na data atual
  - Se data for segunda-feira, incluir sábado/domingo
- Criar modal de cadastro com botão "Lançamento"
- Filtrar apenas accounts com `type="boleto"`

### 4. Nova View: Investments (`/src/views/Investments.py`)

**Criar novo arquivo separado:**
- Mesma estrutura de Expenses
- Filtrar apenas accounts com `type="investment"`
- Tabela com data, valor, descrição e checkbox pago
- Cards de resumo
- Modal de lançamento

### 5. Expenses (`/src/views/Expenses.py`)

**Modificações:**
- Remover tipo "investment" (vai para view separada)
- Manter apenas despesas (`type in ["payment"]`)
- Adicionar checkbox "Pago" em cada entrada
- Adicionar cards de resumo para data atual
- Transformar cadastro em modal via botão "Lançamento"
- Cores: vermelho (não pago) → verde (pago)

### 6. Balances (`/src/views/Balances.py`)

**Modificações:**
- Adicionar coluna "Taxa (%)" na tabela
- Mostrar `interest_rate` de cada banco
- Atualizar formulário de criação/edição:
  - Adicionar input para taxa de juros (%)
  - Passar `interest_rate` ao criar/atualizar banco

### 7. Atualizar Navegação

#### `/src/views/__init__.py`
- Adicionar import de `Investments`

#### `/src/views/Home.py` (se houver menu de navegação)
- Adicionar opção "Investimentos" no menu

### 8. Atualizar Use Cases Frontend

#### Criar `/src/application/use_cases/update_account_paid.py`
```python
def update_account_paid(self, account_id: str, paid: bool) -> Account:
    # PATCH request para /accounts/<id>
    # body: {"paid": paid}
```

#### Atualizar `/src/application/use_cases/account_use_cases.py`
- Adicionar método `update_account`

#### Atualizar `/src/application/use_cases/bank_limit_use_cases.py`
- Adicionar parâmetro `interest_rate` em create e update

## Ordem de Implementação Sugerida

1. ✅ Backend completo
2. ⏳ Entidades frontend (account, bank_limit)
3. ⏳ Balances (mais simples, para testar interest_rate)
4. ⏳ Ticket/Boletos (implementação completa)
5. ⏳ Nova view Investments
6. ⏳ Expenses (ajustar para remover investments)
7. ⏳ Dashboard (adicionar cards)
8. ⏳ Testes finais

## Notas Importantes

- Checkbox "pago": ao clicar, fazer PATCH imediato ao backend
- Cards de "valores a pagar": calcular apenas entries com `paid=False` e data <= hoje
- Segunda-feira: incluir sábado/domingo no cálculo
- Modal de lançamento: usar `@st.dialog` do Streamlit
- Cores: `#DC2626` (vermelho não pago), `#10B981` (verde pago)
