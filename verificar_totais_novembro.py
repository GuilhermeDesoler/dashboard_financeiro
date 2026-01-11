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
    """Converte string de data DD/MM/YYYY para formato DD/MM/YYYY"""
    if not data_str or data_str.strip() == "":
        return None
    try:
        data_obj = datetime.strptime(data_str, "%d/%m/%Y")
        return data_obj.strftime("%d/%m/%Y")
    except ValueError:
        return None

def processar_modalidades_multiplas(modalidade_str):
    """Processa modalidades que vêm juntas (ex: 'Pix Sicoob, Recebimento Crediario')"""
    if not modalidade_str or "," not in modalidade_str:
        return [modalidade_str]
    modalidades = [m.strip() for m in modalidade_str.split(",")]
    return modalidades

# Analisa a planilha
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

print("="*120)
print(f"{'DATA':<15} | {'TOTAL (R$)':>15} | {'QTD':>5}")
print("="*120)

# Calcula total por data
totais_por_data = {}
linhas_dados = linhas[2:]

for idx_data, data in datas:
    total = 0
    qtd = 0

    for idx, linha in enumerate(linhas_dados):
        if len(linha) < 2:
            continue

        col_valor = idx_data * 2
        col_modalidade = idx_data * 2 + 1

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

                # Inclui TUDO, inclusive Crediário
                total += valor_por_modalidade
                qtd += 1

    totais_por_data[data] = total
    print(f"{data:<15} | R$ {total:>12,.2f} | {qtd:>5}")

print("="*120)
print(f"{'TOTAL GERAL':<15} | R$ {sum(totais_por_data.values()):>12,.2f} | {sum([1 for _ in totais_por_data]):>5}")
print("="*120)
