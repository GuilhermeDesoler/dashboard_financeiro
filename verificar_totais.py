import csv
from datetime import datetime
from collections import defaultdict

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

def analisar_planilha(arquivo_csv):
    """Analisa a planilha e conta valores por data"""

    with open(arquivo_csv, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        linhas = list(reader)

    # A primeira linha contém as datas
    header = linhas[0]

    # Extrai as datas
    datas = []
    for i in range(0, len(header), 2):
        data_str = header[i]
        data_formatada = converter_data(data_str)
        if data_formatada:
            datas.append(data_formatada)

    print(f"📅 Datas encontradas: {len(datas)}")

    # Contadores por data
    totais_por_data = defaultdict(lambda: {
        'total_planilha': 0,
        'total_valor_planilha': 0.0,
        'total_nao_crediario': 0,
        'total_valor_nao_crediario': 0.0,
        'total_crediario': 0,
        'total_valor_crediario': 0.0,
    })

    # Pula as duas primeiras linhas
    linhas_dados = linhas[2:]

    # Processa cada linha
    for idx, linha in enumerate(linhas_dados):
        if len(linha) < 2:
            continue

        # Processa cada par valor/modalidade
        for i in range(0, min(len(linha), len(datas) * 2), 2):
            data_idx = i // 2
            if data_idx >= len(datas):
                break

            valor_str = linha[i] if i < len(linha) else ""
            modalidade_str = linha[i + 1] if i + 1 < len(linha) else ""

            valor = limpar_valor(valor_str)
            modalidade = normalizar_modalidade(modalidade_str)

            if valor and modalidade:
                data = datas[data_idx]

                # Conta no total da planilha
                totais_por_data[data]['total_planilha'] += 1
                totais_por_data[data]['total_valor_planilha'] += valor

                # Verifica se é crediário
                if "Crediário" in modalidade or "Crediario" in modalidade:
                    totais_por_data[data]['total_crediario'] += 1
                    totais_por_data[data]['total_valor_crediario'] += valor
                else:
                    totais_por_data[data]['total_nao_crediario'] += 1
                    totais_por_data[data]['total_valor_nao_crediario'] += valor

    return totais_por_data, datas

# Analisa a planilha
arquivo_csv = "Planilha sem título - Página1.csv"
totais, datas = analisar_planilha(arquivo_csv)

print("\n" + "="*100)
print("ANÁLISE DETALHADA POR DATA")
print("="*100)

# Ordena as datas
datas_ordenadas = sorted(totais.keys())

total_geral_planilha = 0
total_geral_nao_crediario = 0
total_geral_crediario = 0

for data in datas_ordenadas[:5]:  # Mostra apenas as primeiras 5 datas
    info = totais[data]
    total_geral_planilha += info['total_planilha']
    total_geral_nao_crediario += info['total_nao_crediario']
    total_geral_crediario += info['total_crediario']

    print(f"\n📅 Data: {data}")
    print(f"   Total na planilha: {info['total_planilha']} lançamentos | R$ {info['total_valor_planilha']:,.2f}")
    print(f"   Não-Crediário (seria importado): {info['total_nao_crediario']} lançamentos | R$ {info['total_valor_nao_crediario']:,.2f}")
    print(f"   Crediário (seria ignorado): {info['total_crediario']} lançamentos | R$ {info['total_valor_crediario']:,.2f}")

print("\n" + "="*100)
print("TOTAIS GERAIS (todas as datas)")
print("="*100)

for data in datas_ordenadas:
    info = totais[data]
    total_geral_planilha += info['total_planilha']
    total_geral_nao_crediario += info['total_nao_crediario']
    total_geral_crediario += info['total_crediario']

print(f"\n📊 Total na planilha: {total_geral_planilha} lançamentos")
print(f"✅ Total NÃO-Crediário (deveria ser importado): {total_geral_nao_crediario} lançamentos")
print(f"⏭️  Total Crediário (deveria ser ignorado): {total_geral_crediario} lançamentos")

print("\n🔍 COMPARAÇÃO COM O RESULTADO DO IMPORT:")
print(f"   Esperado: {total_geral_nao_crediario} lançamentos")
print(f"   Importado: 730 lançamentos")
print(f"   Diferença: {total_geral_nao_crediario - 730} lançamentos")

if total_geral_nao_crediario != 730:
    print("\n⚠️  HÁ UMA DIVERGÊNCIA!")
