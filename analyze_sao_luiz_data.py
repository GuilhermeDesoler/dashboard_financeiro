"""
Script to analyze São Luiz Calçados sales data structure
"""
from collections import defaultdict
import re

# The CSV structure analysis
print("=== ANÁLISE DOS DADOS DE VENDAS - SÃO LUIZ CALÇADOS ===\n")

# Payment modalities found in the data
modalities_found = [
    "Pix Sicredi",
    "Recebimento Crediario",
    "Débito Sicredi",
    "Dinheiro",
    "Parcelado 2 a 4 Sicredi",
    "Crediário",
    "Crédito Av Sicredi",
    "Pix Sicoob",
    "BonusCred",
    "Débito Sicoob",
    "Crédito Av Sicoob",
    "Parcelado 5 a 6 Sicredi",
    "Parcelado 2 a 4 Sicoob",
    "Parcelado 5 a 6 Sicoob"
]

print("MODALIDADES DE PAGAMENTO ENCONTRADAS:")
print("=" * 50)
for i, modality in enumerate(modalities_found, 1):
    print(f"{i:2}. {modality}")

print(f"\nTotal: {len(modalities_found)} modalidades únicas\n")

print("\n=== ESTRUTURA DO ARQUIVO CSV ===")
print("=" * 50)
print("""
Formato: O arquivo contém vendas diárias de Dezembro/2025

Estrutura por linha:
- Cada linha representa múltiplas transações do mesmo dia
- Formato alternado: Valor, Modalidade, Valor, Modalidade, ...
- Cada par de colunas representa uma venda em uma data específica

Header (linha 2):
- Colunas pares: Datas (01/12/2025, 02/12/2025, etc.)
- Colunas ímpares: "Modalidade"

Dados (linhas 3+):
- Colunas pares: Valores (ex: "R$ 89,99")
- Colunas ímpares: Modalidade de pagamento

Total de Vendas do Mês: R$ 228.483,05
""")

print("\n=== MAPEAMENTO PARA O SISTEMA ===")
print("=" * 50)
print("""
1. EMPRESA:
   - Nome: São Luiz Calçados
   - Criar nova empresa no sistema

2. MODALIDADES DE PAGAMENTO:
   - Criar 14 modalidades de pagamento
   - Cada modalidade com cor específica

3. LANÇAMENTOS FINANCEIROS:
   - Tipo: Receita (entrada)
   - Data: Data da venda (coluna do CSV)
   - Valor: Valor da transação
   - Modalidade: Modalidade de pagamento
   - Descrição: "Venda - [Modalidade]"

4. PROCESSAMENTO:
   - Ler cada linha do CSV
   - Para cada par (valor, modalidade) em cada data
   - Criar um lançamento financeiro do tipo "receita"
""")

print("\n=== SUGESTÃO DE CORES PARA MODALIDADES ===")
print("=" * 50)

color_suggestions = {
    "Pix Sicredi": "#00C853",           # Verde escuro
    "Pix Sicoob": "#00E676",            # Verde claro
    "Débito Sicredi": "#2196F3",        # Azul
    "Débito Sicoob": "#03A9F4",         # Azul claro
    "Crédito Av Sicredi": "#FF9800",    # Laranja
    "Crédito Av Sicoob": "#FFB74D",     # Laranja claro
    "Dinheiro": "#4CAF50",              # Verde
    "Crediário": "#9C27B0",             # Roxo
    "Recebimento Crediario": "#BA68C8", # Roxo claro
    "BonusCred": "#E91E63",             # Rosa
    "Parcelado 2 a 4 Sicredi": "#FF5722", # Vermelho
    "Parcelado 5 a 6 Sicredi": "#F44336", # Vermelho escuro
    "Parcelado 2 a 4 Sicoob": "#FF6F00",  # Laranja escuro
    "Parcelado 5 a 6 Sicoob": "#FF8F00"   # Laranja médio
}

for modality, color in color_suggestions.items():
    print(f"  {modality:30} -> {color}")

print("\n" + "=" * 50)
print("PRÓXIMOS PASSOS:")
print("1. Criar empresa 'São Luiz Calçados'")
print("2. Criar as 14 modalidades de pagamento")
print("3. Importar os lançamentos do CSV")
print("=" * 50)
