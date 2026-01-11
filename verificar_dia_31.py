import csv
import requests
from datetime import datetime
from collections import defaultdict

# Token de autenticação
AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYzkxMzY2YmUtMDIzMC00OTJkLTk4OTUtMTI2NjhlYTZjYzA0IiwiZW1haWwiOiJzdXBlckB0ZXN0ZS5jb20iLCJuYW1lIjoiU3VwZXIgQWRtaW4iLCJjb21wYW55X2lkIjpudWxsLCJyb2xlcyI6W10sImZlYXR1cmVzIjpbXSwiaXNfc3VwZXJfYWRtaW4iOnRydWUsImV4cCI6MTc2ODE4Nzg5MCwiaWF0IjoxNzY4MTAxNDkwfQ.X1NYrmFMk3WSy8sC29YgygxoQb8VZEodim3p3nangyk"

def limpar_valor(valor_str):
    """Converte string de valor brasileiro para float"""
    if not valor_str or valor_str.strip() == "" or valor_str.strip() == "\\":
        return None
    valor_str = valor_str.replace("R$", "").strip()
    valor_str = valor_str.replace(".", "")
    valor_str = valor_str.replace(",", ".")
    try:
        return float(valor_str)
    except ValueError:
        return None

def normalizar_modalidade(modalidade_str):
    """Normaliza o nome da modalidade"""
    if not modalidade_str or modalidade_str.strip() == "":
        return None
    modalidade_str = modalidade_str.strip()
    if modalidade_str == "Modalidade":
        return None
    replacements = {
        "Ã©": "é",
        "Ã¡": "á",
        "Ã­": "í",
        "Ã³": "ó",
        "DÃ©bito": "Débito",
        "CrÃ©dito": "Crédito",
        "CrediÃ¡rio": "Crediário",
    }
    for old, new in replacements.items():
        modalidade_str = modalidade_str.replace(old, new)
    return modalidade_str

def converter_data(data_str):
    """Converte string de data DD/MM/YYYY para formato YYYY-MM-DD"""
    if not data_str or data_str.strip() == "":
        return None
    try:
        data_obj = datetime.strptime(data_str, "%d/%m/%Y")
        return data_obj.strftime("%Y-%m-%d")
    except ValueError:
        return None

# Analisa a planilha para o dia 31/12
arquivo_csv = "Planilha sem título - Página1.csv"

with open(arquivo_csv, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    linhas = list(reader)

header = linhas[0]

# Extrai as datas
datas = []
for i in range(0, len(header), 2):
    data_str = header[i]
    data_formatada = converter_data(data_str)
    if data_formatada:
        datas.append((i // 2, data_formatada))

# Encontra o índice do dia 31/12
dia_31_idx = None
for idx, data in datas:
    if data == "2025-12-31":
        dia_31_idx = idx
        break

if dia_31_idx is None:
    print("❌ Dia 31/12/2025 não encontrado na planilha")
    exit(1)

print("="*100)
print(f"📅 ANÁLISE DO DIA 31/12/2025 (índice {dia_31_idx})")
print("="*100)

# Extrai todos os lançamentos do dia 31/12 da planilha
lancamentos_planilha = []
linhas_dados = linhas[2:]

for idx, linha in enumerate(linhas_dados):
    if len(linha) < 2:
        continue

    col_valor = dia_31_idx * 2
    col_modalidade = dia_31_idx * 2 + 1

    if col_valor >= len(linha):
        continue

    valor_str = linha[col_valor] if col_valor < len(linha) else ""
    modalidade_str = linha[col_modalidade] if col_modalidade < len(linha) else ""

    valor = limpar_valor(valor_str)
    modalidade = normalizar_modalidade(modalidade_str)

    if valor and modalidade:
        eh_crediario = "Crediário" in modalidade or "Crediario" in modalidade
        lancamentos_planilha.append({
            'valor': valor,
            'modalidade': modalidade,
            'crediario': eh_crediario
        })

print(f"\n📋 LANÇAMENTOS NA PLANILHA (dia 31/12):")
print(f"{'Valor':>15} | {'Modalidade':<30} | Crediário")
print("-" * 100)

total_planilha = 0
total_nao_crediario = 0
valor_total_planilha = 0
valor_total_nao_crediario = 0

for lanc in lancamentos_planilha:
    print(f"R$ {lanc['valor']:>10,.2f} | {lanc['modalidade']:<30} | {'Sim' if lanc['crediario'] else 'Não'}")
    total_planilha += 1
    valor_total_planilha += lanc['valor']
    if not lanc['crediario']:
        total_nao_crediario += 1
        valor_total_nao_crediario += lanc['valor']

print("-" * 100)
print(f"{'TOTAL PLANILHA:':>15} {total_planilha} lançamentos | R$ {valor_total_planilha:,.2f}")
print(f"{'NÃO-CREDIÁRIO:':>15} {total_nao_crediario} lançamentos | R$ {valor_total_nao_crediario:,.2f}")

# Busca os lançamentos do banco para 31/12
print(f"\n\n📊 LANÇAMENTOS NO BANCO (dia 31/12):")
print("-" * 100)

API_BASE_URL = "http://localhost:5000"
headers = {
    "Authorization": f"Bearer {AUTH_TOKEN}",
    "Content-Type": "application/json"
}

try:
    response = requests.get(
        f"{API_BASE_URL}/api/financial-entries",
        params={"start_date": "2025-12-31", "end_date": "2025-12-31"},
        headers=headers,
        timeout=30
    )
    response.raise_for_status()
    lancamentos_banco = response.json()

    print(f"{'Valor':>15} | {'Modalidade':<30}")
    print("-" * 100)

    total_banco = 0
    valor_total_banco = 0

    for lanc in lancamentos_banco:
        valor = lanc.get('value', 0)
        modalidade = lanc.get('modality_name', 'N/A')
        print(f"R$ {valor:>10,.2f} | {modalidade:<30}")
        total_banco += 1
        valor_total_banco += valor

    print("-" * 100)
    print(f"{'TOTAL BANCO:':>15} {total_banco} lançamentos | R$ {valor_total_banco:,.2f}")

    print("\n" + "="*100)
    print("COMPARAÇÃO:")
    print("="*100)
    print(f"Planilha (não-crediário): {total_nao_crediario} lançamentos | R$ {valor_total_nao_crediario:,.2f}")
    print(f"Banco:                     {total_banco} lançamentos | R$ {valor_total_banco:,.2f}")
    print(f"Diferença:                 {total_banco - total_nao_crediario} lançamentos | R$ {valor_total_banco - valor_total_nao_crediario:,.2f}")

    if total_banco > total_nao_crediario:
        print("\n⚠️  O BANCO TEM MAIS LANÇAMENTOS QUE A PLANILHA!")
        print("Possíveis causas:")
        print("  1. Lançamentos duplicados foram importados")
        print("  2. Há lançamentos antigos no banco que não estão na planilha")

except Exception as e:
    print(f"❌ Erro ao buscar dados do banco: {str(e)}")
