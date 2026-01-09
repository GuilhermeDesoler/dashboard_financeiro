# Guia de Importação - São Luiz Calçados

Este documento descreve o processo completo para importar os dados de vendas da São Luiz Calçados no sistema.

## 📊 Resumo dos Dados

- **Arquivo**: `Cópia de Financeiro São Luiz Calçados - Vendas Dezembro_25.csv`
- **Período**: Dezembro de 2025
- **Total de Vendas**: R$ 228.483,05
- **Modalidades de Pagamento**: 14 modalidades diferentes

## 🏢 Modalidades de Pagamento

O arquivo contém as seguintes modalidades de pagamento:

| # | Modalidade | Tipo | Cor Sugerida |
|---|------------|------|--------------|
| 1 | Pix Sicredi | PIX | #00C853 (Verde escuro) |
| 2 | Pix Sicoob | PIX | #00E676 (Verde claro) |
| 3 | Débito Sicredi | Débito | #2196F3 (Azul) |
| 4 | Débito Sicoob | Débito | #03A9F4 (Azul claro) |
| 5 | Crédito Av Sicredi | Crédito | #FF9800 (Laranja) |
| 6 | Crédito Av Sicoob | Crédito | #FFB74D (Laranja claro) |
| 7 | Dinheiro | Dinheiro | #4CAF50 (Verde) |
| 8 | Crediário | Crediário | #9C27B0 (Roxo) |
| 9 | Recebimento Crediario | Crediário | #BA68C8 (Roxo claro) |
| 10 | BonusCred | Crédito | #E91E63 (Rosa) |
| 11 | Parcelado 2 a 4 Sicredi | Parcelado | #FF5722 (Vermelho) |
| 12 | Parcelado 5 a 6 Sicredi | Parcelado | #F44336 (Vermelho escuro) |
| 13 | Parcelado 2 a 4 Sicoob | Parcelado | #FF6F00 (Laranja escuro) |
| 14 | Parcelado 5 a 6 Sicoob | Parcelado | #FF8F00 (Laranja médio) |

## 📝 Estrutura do CSV

O arquivo CSV tem uma estrutura especial:

```
Linha 1: Total de vendas do mês
Linha 2: Cabeçalhos (datas alternadas com "Modalidade")
Linha 3: Linha vazia
Linhas 4+: Dados das vendas
```

### Formato das Colunas

- **Colunas pares (0, 2, 4, ...)**: Datas (01/12/2025, 02/12/2025, etc.)
- **Colunas ímpares (1, 3, 5, ...)**: "Modalidade"

### Formato dos Dados

Cada linha de dados contém múltiplas transações:

```
"R$ 89,99", "Pix Sicredi", "R$ 35,75", "Recebimento Crediario", ...
  Valor 1    Modalidade 1     Valor 2      Modalidade 2
```

## 🚀 Processo de Importação

### Passo 1: Criar a Empresa

1. Faça login como Super Admin
2. Vá para a página **Admin**
3. Na seção **Empresas**, clique em **Criar Empresa**
4. Preencha:
   - **Nome**: `São Luiz Calçados`
5. Clique em **Criar**
6. **⚠️ IMPORTANTE**: Copie o **company_id** da empresa criada (você precisará dele no próximo passo)

### Passo 2: Configurar o Script de Importação

1. Abra o arquivo `import_sao_luiz_data.py`
2. Localize a linha:
   ```python
   COMPANY_ID = "YOUR_COMPANY_ID_HERE"
   ```
3. Substitua `"YOUR_COMPANY_ID_HERE"` pelo company_id copiado no Passo 1
4. Salve o arquivo

### Passo 3: Executar em Modo Dry Run (Teste)

Primeiro, execute o script em modo de teste para verificar os dados:

```bash
python3 import_sao_luiz_data.py
```

O script irá:
- ✅ Mostrar as modalidades que seriam criadas
- ✅ Mostrar as primeiras 10 transações que seriam importadas
- ✅ Mostrar um resumo completo dos dados
- ❌ **NÃO irá fazer nenhuma alteração no banco de dados**

### Passo 4: Revisar a Saída

Verifique se:
- As 14 modalidades estão corretas
- As transações têm valores e datas corretos
- O total de vendas está próximo de R$ 228.483,05

### Passo 5: Executar a Importação Real

Se tudo estiver correto no dry run:

1. Abra o arquivo `import_sao_luiz_data.py`
2. Localize a linha:
   ```python
   DRY_RUN = True
   ```
3. Altere para:
   ```python
   DRY_RUN = False
   ```
4. Salve o arquivo
5. Execute novamente:
   ```bash
   python3 import_sao_luiz_data.py
   ```

O script irá:
1. Criar as 14 modalidades de pagamento
2. Importar todas as transações de vendas
3. Mostrar um resumo com:
   - Total de transações importadas
   - Valor total importado
   - Breakdown por modalidade

## 📊 Após a Importação

Depois que a importação for concluída com sucesso:

1. Faça login como Super Admin
2. Use a funcionalidade de **Impersonar** para acessar a empresa "São Luiz Calçados"
3. Verifique no Dashboard:
   - O total de receitas do mês
   - As modalidades de pagamento criadas
   - Os lançamentos individuais

## 🔍 Verificação de Dados

Para verificar se a importação foi bem-sucedida:

### 1. Total Esperado
- **Valor Total**: R$ 228.483,05
- **Período**: 01/12/2025 a 31/12/2025

### 2. Verificar Modalidades
- Vá para **Modalidades** e confirme que existem 14 modalidades
- Cada uma deve ter sua cor específica

### 3. Verificar Lançamentos
- Vá para **Dashboard** ou **Receitas**
- Filtre por dezembro de 2025
- Verifique se o total bate com o esperado

## ⚠️ Troubleshooting

### Problema: "ModuleNotFoundError"

**Solução**: Certifique-se de estar executando o script no diretório correto:
```bash
cd /Users/primum/financeiros/dashboard_financeiro
python3 import_sao_luiz_data.py
```

### Problema: "FileNotFoundError" para o CSV

**Solução**: Coloque o arquivo CSV no mesmo diretório do script:
```bash
# O arquivo deve estar em:
/Users/primum/financeiros/dashboard_financeiro/Cópia de Financeiro São Luiz Calçados - Vendas Dezembro_25.csv
```

### Problema: "Company ID not found"

**Solução**:
1. Verifique se você criou a empresa no Admin
2. Copie o company_id correto da URL ou da lista de empresas
3. Atualize o script com o ID correto

### Problema: Modalidades duplicadas

**Solução**: Se você executar o script duas vezes, pode criar modalidades duplicadas. Para resolver:
1. Vá para a página de Modalidades
2. Exclua as modalidades duplicadas
3. Execute o script novamente em modo dry run primeiro

## 📚 Arquivos Relacionados

- `import_sao_luiz_data.py` - Script principal de importação
- `analyze_sao_luiz_data.py` - Script de análise dos dados
- `Cópia de Financeiro São Luiz Calçados - Vendas Dezembro_25.csv` - Arquivo de dados

## 📞 Suporte

Se encontrar problemas durante a importação, verifique:

1. ✅ O arquivo CSV está no local correto
2. ✅ O company_id foi atualizado no script
3. ✅ Você executou primeiro em modo dry run
4. ✅ As dependências do sistema estão instaladas
5. ✅ Você tem permissão de Super Admin

## 🎯 Próximos Passos

Após a importação bem-sucedida:

1. **Criar Usuários**: Crie usuários para os funcionários da São Luiz Calçados
2. **Configurar Permissões**: Configure as permissões de cada usuário
3. **Treinar Equipe**: Mostre como usar o sistema
4. **Importar Outros Meses**: Use o mesmo processo para importar dados de outros meses

---

**Data de Criação**: Janeiro 2026
**Versão**: 1.0
**Status**: Pronto para uso
