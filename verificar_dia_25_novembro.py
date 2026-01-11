import csv
from datetime import datetime

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

def processar_modalidades_multiplas(modalidade_str):
    """Processa modalidades que vêm juntas (ex: 'Pix Sicoob, Recebimento Crediario')"""
    if not modalidade_str or "," not in modalidade_str:
        return [modalidade_str]
    modalidades = [m.strip() for m in modalidade_str.split(",")]
    return modalidades

# Analisa a planilha para o dia 25/11
arquivo_csv = "cop-novembro.csv"

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

# Encontra o índice do dia 25/11
dia_25_idx = None
for idx, data in datas:
    if data == "2025-11-25":
        dia_25_idx = idx
        break

if dia_25_idx is None:
    print("❌ Dia 25/11/2025 não encontrado na planilha")
    exit(1)

print("="*100)
print(f"📅 ANÁLISE DO DIA 25/11/2025 (índice {dia_25_idx})")
print("="*100)

# Extrai todos os lançamentos do dia 25/11 da planilha
lancamentos_planilha = []
linhas_dados = linhas[2:]

for idx, linha in enumerate(linhas_dados):
    if len(linha) < 2:
        continue

    col_valor = dia_25_idx * 2
    col_modalidade = dia_25_idx * 2 + 1

    if col_valor >= len(linha):
        continue

    valor_str = linha[col_valor] if col_valor < len(linha) else ""
    modalidade_str = linha[col_modalidade] if col_modalidade < len(linha) else ""

    valor = limpar_valor(valor_str)
    modalidade = normalizar_modalidade(modalidade_str)

    if valor and modalidade:
        # Processa modalidades múltiplas
        modalidades = processar_modalidades_multiplas(modalidade)
        valor_por_modalidade = valor / len(modalidades)

        for mod in modalidades:
            mod = mod.strip()
            if not mod:
                continue

            eh_crediario = "Crediário" in mod or "Crediario" in mod
            # Exceto "Recebimento Crediario"
            if eh_crediario and "Recebimento" not in mod:
                continue  # Ignora crediários

            lancamentos_planilha.append({
                'valor': valor_por_modalidade,
                'modalidade': mod,
                'crediario': eh_crediario and "Recebimento" not in mod
            })

print(f"\n📋 LANÇAMENTOS NA PLANILHA (dia 25/11) - NÃO CREDIÁRIO:")
print(f"{'Valor':>15} | {'Modalidade':<40}")
print("-" * 100)

total_nao_crediario = 0
valor_total_nao_crediario = 0

for lanc in lancamentos_planilha:
    print(f"R$ {lanc['valor']:>10,.2f} | {lanc['modalidade']:<40}")
    total_nao_crediario += 1
    valor_total_nao_crediario += lanc['valor']

print("-" * 100)
print(f"{'TOTAL:':>15} {total_nao_crediario} lançamentos | R$ {valor_total_nao_crediario:,.2f}")
print("="*100)
