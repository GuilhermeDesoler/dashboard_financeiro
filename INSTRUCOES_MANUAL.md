# Instruções para Importação Manual - São Luiz Calçados

Como o script automático precisa de autenticação da API, aqui estão as instruções para fazer a importação manualmente através da interface web.

## 📋 Resumo do que será criado

- **1 Empresa**: São Luiz Calçados
- **14 Modalidades de Pagamento** com cores específicas
- **~500-1000 Transações** de vendas de Dezembro/2025
- **Total**: R$ 228.483,05

---

## PASSO 1: Criar a Empresa

1. Faça login como **Super Admin**
2. Vá para a página **Admin**
3. Na seção **Empresas**, clique em **Criar Empresa**
4. Preencha:
   - **Nome**: `São Luiz Calçados`
   - **CNPJ**: (deixe vazio)
   - **Telefone**: (deixe vazio)
   - **Plano**: basic
5. Clique em **Criar**
6. **⚠️ IMPORTANTE**: Copie o **company_id** da empresa criada

---

## PASSO 2: Impersonar a Empresa

1. Na lista de empresas, clique em **Impersonar** na empresa "São Luiz Calçados"
2. Você será redirecionado para o dashboard da empresa

---

## PASSO 3: Criar as Modalidades de Pagamento

Vá para **Modalidades** e crie cada uma das 14 modalidades abaixo **NA ORDEM**:

### Modalidade 1: Pix Sicredi
- Nome: `Pix Sicredi`
- Cor: `#00C853`
- Clique em **Criar**

### Modalidade 2: Pix Sicoob
- Nome: `Pix Sicoob`
- Cor: `#00E676`
- Clique em **Criar**

### Modalidade 3: Débito Sicredi
- Nome: `Débito Sicredi`
- Cor: `#2196F3`
- Clique em **Criar**

### Modalidade 4: Débito Sicoob
- Nome: `Débito Sicoob`
- Cor: `#03A9F4`
- Clique em **Criar**

### Modalidade 5: Crédito Av Sicredi
- Nome: `Crédito Av Sicredi`
- Cor: `#FF9800`
- Clique em **Criar**

### Modalidade 6: Crédito Av Sicoob
- Nome: `Crédito Av Sicoob`
- Cor: `#FFB74D`
- Clique em **Criar**

### Modalidade 7: Dinheiro
- Nome: `Dinheiro`
- Cor: `#4CAF50`
- Clique em **Criar**

### Modalidade 8: Crediário
- Nome: `Crediário`
- Cor: `#9C27B0`
- Clique em **Criar**

### Modalidade 9: Recebimento Crediario
- Nome: `Recebimento Crediario`
- Cor: `#BA68C8`
- Clique em **Criar**

### Modalidade 10: BonusCred
- Nome: `BonusCred`
- Cor: `#E91E63`
- Clique em **Criar**

### Modalidade 11: Parcelado 2 a 4 Sicredi
- Nome: `Parcelado 2 a 4 Sicredi`
- Cor: `#FF5722`
- Clique em **Criar**

### Modalidade 12: Parcelado 5 a 6 Sicredi
- Nome: `Parcelado 5 a 6 Sicredi`
- Cor: `#F44336`
- Clique em **Criar**

### Modalidade 13: Parcelado 2 a 4 Sicoob
- Nome: `Parcelado 2 a 4 Sicoob`
- Cor: `#FF6F00`
- Clique em **Criar**

### Modalidade 14: Parcelado 5 a 6 Sicoob
- Nome: `Parcelado 5 a 6 Sicoob`
- Cor: `#FF8F00`
- Clique em **Criar**

✅ **Verifique**: Você deve ter 14 modalidades criadas

---

## PASSO 4: Importar as Transações

Agora que a empresa e as modalidades estão criadas, você pode usar o script de importação:

### Opção A: Script Python (Recomendado)

1. Saia do modo de impersonação
2. Abra o arquivo `import_with_company_id.py` (vou criar para você)
3. Atualize o `COMPANY_ID` com o ID copiado no Passo 1
4. Execute:
   ```bash
   source .venv/bin/activate
   PYTHONPATH=/Users/primum/financeiros/dashboard_financeiro/src python3 import_with_company_id.py
   ```

### Opção B: Importação Manual (Demorada)

Se o script não funcionar, você pode importar manualmente através da interface:

1. Vá para **Receitas** ou **Dashboard**
2. Clique em **Novo Lançamento**
3. Para cada transação no CSV:
   - Data: (data da venda)
   - Valor: (valor da venda)
   - Descrição: "Venda - [Modalidade]"
   - Modalidade: (selecione a modalidade correspondente)
   - Clique em **Salvar**

⚠️ **ATENÇÃO**: Esta opção é muito demorada pois são centenas de transações!

---

## ✅ Verificação Final

Após a importação:

1. Vá para **Dashboard**
2. Selecione o período de **01/12/2025 a 31/12/2025**
3. Verifique se:
   - ✅ O total de receitas é aproximadamente **R$ 228.483,05**
   - ✅ As 14 modalidades aparecem nos filtros
   - ✅ Há transações distribuídas ao longo do mês

---

## 🆘 Problemas?

### "Empresa já existe"
- Verifique na lista de empresas se "São Luiz Calçados" já foi criada
- Se sim, use o ID da empresa existente

### "Modalidade já existe"
- Vá para Modalidades e verifique quais já foram criadas
- Pule as que já existem e crie apenas as faltantes

### "Erro ao importar transações"
- Verifique se todas as 14 modalidades foram criadas
- Verifique se o company_id está correto no script

---

## 📞 Próximos Passos

Após concluir a importação:

1. **Criar usuários** para os funcionários da São Luiz Calçados
2. **Configurar permissões** de cada usuário
3. **Treinar a equipe** no uso do sistema
4. **Importar dados** de outros meses (se houver)

---

**Criado em**: Janeiro 2026
**Status**: Pronto para uso
