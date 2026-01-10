# 📊 Guia de Importação - São Luiz Calçados

Este documento descreve o processo completo de importação de dados da empresa **São Luiz Calçados** para o sistema de Dashboard Financeiro.

## 🎯 Visão Geral

A importação completa inclui os seguintes tipos de dados:

- ✅ **Vendas** (Novembro/2025, Dezembro/2025, Janeiro/2026)
- 💸 **Despesas** (2025 e 2026)
- 💳 **Crediário** (2025 e 2026) - Vendas a prazo com parcelamento
- 🧾 **Boletos** (2025 e 2026) - Contas a pagar
- 💰 **Empréstimos** - Saldo de empréstimos bancários
- 📈 **Investimentos** - Aplicações financeiras
- 🏦 **Saldos e Limites Bancários** - Limites de crédito disponíveis

## 📋 Pré-requisitos

### 1. Empresa Criada
A empresa **São Luiz Calçados** deve estar criada no sistema:
- **Company ID**: `9848381a-7b78-4d3e-a781-cd94fdcf8236`
- **Database**: `cmp_57280b31_db`
- **Status**: Ativa

### 2. Modalidades de Pagamento
14 modalidades devem estar criadas:
1. Pix Sicredi
2. Pix Sicoob
3. Débito Sicredi
4. Débito Sicoob
5. Crédito Av Sicredi
6. Crédito Av Sicoob
7. Dinheiro
8. Crediário
9. Recebimento Crediario
10. BonusCred
11. Parcelado 2 a 4 Sicredi
12. Parcelado 5 a 6 Sicredi
13. Parcelado 2 a 4 Sicoob
14. Parcelado 5 a 6 Sicoob

### 3. Acesso Super Admin
Apenas super administradores podem executar a importação.

## 🚀 Métodos de Importação

### Método 1: Interface Streamlit (Recomendado)

#### Passo 1: Acessar o Sistema
```bash
cd /Users/primum/financeiros/dashboard_financeiro
source .venv/bin/activate
streamlit run src/main.py
```

#### Passo 2: Fazer Login como Super Admin
- Acesse a página de Login
- Entre com suas credenciais de super admin

#### Passo 3: Impersonar a Empresa
1. Vá para a página **Admin**
2. Encontre **São Luiz Calçados** na lista de empresas
3. Clique em **Impersonar**
4. Você verá um timer indicando que está impersonando

#### Passo 4: Acessar a Página de Importação
- No menu lateral, clique em **Import Completo**
- A página mostrará 5 abas para diferentes tipos de importação

#### Passo 5: Importar Dados por Tipo

**Aba 1: Vendas**
1. Faça upload de cada arquivo CSV de vendas:
   - `Vendas Novembro_25.csv` (R$ 116.421,84)
   - `Vendas Dezembro_25.csv` (R$ 228.483,05)
   - `Vendas Janeiro_26.csv` (R$ 15.074,41)
2. Clique em **Importar Vendas**
3. Aguarde a confirmação
4. Repita para cada arquivo

**Aba 2: Empréstimos**
1. Faça upload de `Emprestimos.csv`
2. Clique em **Importar Empréstimos**
3. Verifique o total: R$ 97.928,00

**Aba 3: Investimentos**
1. Faça upload de `Investimentos.csv`
2. Clique em **Importar Investimentos**
3. Verifique o total: R$ 76.476,31

**Aba 4: Limites Bancários**
1. Faça upload de `Saldos e Taxas.csv`
2. Clique em **Importar Limites**
3. Verifique os limites criados:
   - Sicredi Rotativo: R$ 80.000,00
   - Sicredi Cheque Especial: R$ 5.000,00
   - Sicoob Cheque Especial: R$ 30.000,00

**Aba 5: Resumo**
- Visualize o resumo de todos os dados importados
- Confirme os totais esperados

### Método 2: Script Backend (Avançado)

#### Executar Script Python Completo

```bash
cd /Users/primum/financeiros/back_dashboard_financeiro
source .venv/bin/activate
python scripts/import_sao_luiz_complete.py
```

Este script importa automaticamente todos os CSVs disponíveis no diretório:
`/Users/primum/financeiros/dashboard_financeiro/`

## 📊 Estrutura dos CSVs

### 1. Vendas (Novembro, Dezembro, Janeiro)

**Formato**:
```
Linha 0: Total geral das vendas
Linha 1: Datas (colunas pares) | Modalidade (colunas ímpares)
Linha 2: Vazia
Linhas 3+: Valores por data e modalidade
```

**Exemplo**:
```csv
"R$ 228.483,05"
"01/12/2025","Modalidade","02/12/2025","Modalidade",...
""
"R$ 1.234,56","Pix Sicredi","R$ 890,00","Débito Sicoob",...
```

**Encoding**: UTF-8 com possíveis problemas (Ã© → é, Ã¡ → á)

### 2. Empréstimos

**Formato**: CSV com colunas
```csv
Banco,Saldo
Sicredi,"R$ 97.928,00"
```

### 3. Investimentos

**Formato**: CSV com colunas
```csv
Banco,Valor,Tipo,Objetivo
Sicredi,"R$ 50.000,00",Poupança,Garantia
Sicoob,"R$ 26.476,31",CDB,Reserva
```

### 4. Saldos e Limites

**Formato**: CSV com colunas
```csv
Banco,Tipo,Limite,Taxa
Sicredi,Rotativo,"R$ 80.000,00","5,5%"
Sicredi,Cheque Especial,"R$ 5.000,00","8,2%"
Sicoob,Cheque Especial,"R$ 30.000,00","7,8%"
```

### 5. Despesas (2025 e 2026)

**Formato**: Colunas por mês
```csv
Novembro,Dezembro,Janeiro,...
Data | Descrição | Valor | Status
```

**Status**: "Pago" ou "Em aberto"

### 6. Crediário (2025 e 2026)

**Formato**: Tracking mensal
```csv
Data,Venda,Recebido,Em Aberto
01/11/2025,"R$ 5.000,00","R$ 1.000,00","R$ 4.000,00"
```

### 7. Boletos (2025 e 2026)

**Formato**: Por dia do mês
```csv
Dia,Valor,Descrição
1,"R$ 2.500,00",Fornecedor XYZ
15,"R$ 1.800,00",Aluguel
```

## 🔍 Validações

Durante a importação, o sistema valida:

1. **Formato de Moeda**: R$ 1.234,56 → 1234.56
2. **Formato de Data**: DD/MM/YYYY
3. **Modalidades**: Todas as modalidades devem existir no sistema
4. **Encoding**: Corrige automaticamente problemas de UTF-8
5. **Valores**: Apenas valores positivos são importados
6. **Company ID**: Verifica se está impersonando a empresa correta

## 📈 Resultados Esperados

Após a importação completa, você deve ter:

### Vendas
- **Total**: ~R$ 360.000,00
- **Período**: Novembro/2025 a Janeiro/2026
- **Transações**: ~1.500-2.000 vendas

### Despesas
- **2025**: R$ 112.549,50 (Novembro + Dezembro)
- **2026**: R$ 33.338,77 (Janeiro)

### Boletos
- **2025**: R$ 225.192,91 (Novembro + Dezembro)
- **2026**: R$ 71.993,81 (Janeiro a Março)

### Empréstimos
- **Total**: R$ 97.928,00
- **Banco**: Sicredi

### Investimentos
- **Total**: R$ 76.476,31
- **Aplicações**: 2 investimentos

### Limites Bancários
- **Sicredi**: R$ 85.000,00 (R$ 80k rotativo + R$ 5k cheque)
- **Sicoob**: R$ 30.000,00 (cheque especial)

## 🔧 Troubleshooting

### Problema: "Empresa não encontrada"
**Solução**: Verifique se a empresa foi criada executando:
```bash
python scripts/seed_sao_luiz.py
```

### Problema: "Modalidade não encontrada"
**Solução**: As 14 modalidades devem estar no banco. Execute o seed novamente.

### Problema: "0 transações importadas"
**Solução**:
1. Verifique o formato do CSV
2. Confirme que está impersonando a empresa correta (pelo ID, não pelo nome)
3. Verifique encoding do arquivo (deve ser UTF-8)

### Problema: "Erro de encoding (Ã©, Ã¡)"
**Solução**: O sistema corrige automaticamente, mas se persistir:
```python
# Abra o CSV e salve com encoding UTF-8
import pandas as pd
df = pd.read_csv('arquivo.csv', encoding='latin1')
df.to_csv('arquivo_utf8.csv', encoding='utf-8', index=False)
```

### Problema: "Acesso negado"
**Solução**: Apenas super admins podem importar. Verifique:
```python
current_user.is_super_admin == True
```

## 📝 Mapeamento de Entidades

### FinancialEntry
- **Vendas**: `entry_type="normal"`, `type="received"`
- **Despesas**: `entry_type="despesa"`, `type="received"`
- **Empréstimos**: `entry_type="emprestimo"`, `type="received"`
- **Crediário**: `is_credit_plan=True`, `type="receivable"`

### Account
- **Boletos**: `type="boleto"`
- **Investimentos**: `type="investment"`

### Installment
- Criado automaticamente para crediário
- Liga-se ao `financial_entry_id`
- Rastreia parcelas individuais

### BankLimit
- **Rotativo**: `rotativo_available`, `rotativo_used`
- **Cheque Especial**: `cheque_available`, `cheque_used`
- **Taxas**: `rotativo_rate`, `cheque_rate`

## ✅ Verificação Pós-Importação

### 1. Dashboard
- Acesse **Dashboard**
- Filtre por **Dezembro/2025**
- Verifique total de vendas: ~R$ 228.483,05

### 2. Lançamentos
- Acesse **Lançamentos**
- Filtre por modalidade
- Confirme distribuição de vendas

### 3. Saldos e Limites
- Acesse **Saldos e Limites**
- Verifique limites bancários criados
- Confirme valores disponíveis

### 4. Boletos
- Acesse **Boletos**
- Verifique contas a pagar
- Confirme datas de vencimento

### 5. Investimentos
- Acesse **Investimentos**
- Confirme R$ 76.476,31 total

## 🎓 Notas Importantes

1. **Não deletar dados existentes**: A importação adiciona novos dados, não sobrescreve
2. **IDs únicos**: Cada transação recebe um ID único do MongoDB
3. **Timestamps**: Todas as entidades têm `created_at` e `updated_at`
4. **Multitenancy**: Dados isolados por empresa (database separado)
5. **Impersonation**: Token expira em 1 hora, renovar se necessário

## 📞 Suporte

Para problemas ou dúvidas:
1. Verifique os logs do sistema
2. Consulte a documentação técnica do backend
3. Execute testes com CSVs menores primeiro
4. Valide os dados manualmente após importação

---

**Última atualização**: Janeiro 2026
**Versão**: 1.0.0
