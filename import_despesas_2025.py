import csv
import requests
from datetime import datetime

# Configurações da API
API_BASE_URL = "http://localhost:5000"
API_ENDPOINT = f"{API_BASE_URL}/api/accounts"

# Token de autenticação
AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYzkxMzY2YmUtMDIzMC00OTJkLTk4OTUtMTI2NjhlYTZjYzA0IiwiZW1haWwiOiJzdXBlckB0ZXN0ZS5jb20iLCJuYW1lIjoiU3VwZXIgQWRtaW4iLCJjb21wYW55X2lkIjpudWxsLCJyb2xlcyI6W10sImZlYXR1cmVzIjpbXSwiaXNfc3VwZXJfYWRtaW4iOnRydWUsImV4cCI6MTc2ODE4Nzg5MCwiaWF0IjoxNzY4MTAxNDkwfQ.X1NYrmFMk3WSy8sC29YgygxoQb8VZEodim3p3nangyk"


def limpar_valor(valor_str):
    """Converte string de valor brasileiro para float"""
    if not valor_str or valor_str.strip() == "":
        return None
    valor_str = valor_str.replace("R$", "").strip()
    valor_str = valor_str.replace(".", "")
    valor_str = valor_str.replace(",", ".")
    try:
        return float(valor_str)
    except ValueError:
        return None


def normalizar_descricao(desc_str):
    """Normaliza descrição corrigindo problemas de encoding"""
    if not desc_str or desc_str.strip() == "":
        return None

    desc_str = desc_str.strip()

    # Corrigir problemas de encoding
    replacements = {
        "Ã©": "é",
        "Ã¡": "á",
        "Ã­": "í",
        "Ã³": "ó",
        "Ãº": "ú",
        "Ã£": "ã",
        "Ã§": "ç",
        "Ã‰": "É",
        "Ã": "Á",
        "Ãª": "ê",
        "Ã´": "ô",
        "Â°": "°",
    }

    for old, new in replacements.items():
        desc_str = desc_str.replace(old, new)

    return desc_str


def criar_despesa(data, valor, descricao, paid, dry_run=True):
    """Cria uma despesa via API"""

    # Prepara o payload
    payload = {
        "value": valor,
        "date": data,
        "description": descricao,
        "type": "payment",
        "paid": paid
    }

    if dry_run:
        status_str = "✅ Pago" if paid else "⏳ Em aberto"
        print(f"  🔵 DRY RUN: {data} - R$ {valor:,.2f} - {descricao} - {status_str}")
        return {"status": "dry_run", "payload": payload}

    # Faz a requisição
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(API_ENDPOINT, json=payload, headers=headers)

        if response.status_code in [200, 201]:
            status_str = "✅ Pago" if paid else "⏳ Em aberto"
            print(f"  ✅ SUCESSO: {data} - R$ {valor:,.2f} - {descricao} - {status_str}")
            return {"status": "success", "response": response.json()}
        else:
            print(f"  ❌ ERRO: {data} - R$ {valor:,.2f} - {descricao}")
            print(f"     Status: {response.status_code}")
            print(f"     Resposta: {response.text}")
            return {"status": "error", "status_code": response.status_code, "response": response.text}

    except Exception as e:
        print(f"  ❌ EXCEÇÃO: {data} - R$ {valor:,.2f} - {descricao}")
        print(f"     Erro: {str(e)}")
        return {"status": "exception", "error": str(e)}


def processar_csv(arquivo_csv, dry_run=True):
    """Processa o arquivo CSV e cria as despesas"""

    print(f"\n{'='*80}")
    print(f"PROCESSANDO ARQUIVO: {arquivo_csv}")
    print(f"MODO: {'DRY RUN (simulação)' if dry_run else 'EXECUÇÃO REAL'}")
    print(f"{'='*80}\n")

    with open(arquivo_csv, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        linhas = list(reader)

    # A primeira linha contém os nomes dos meses
    header = linhas[0]

    # A partir da segunda linha, temos os dados
    linhas_dados = linhas[1:]

    total_despesas = 0
    total_sucesso = 0
    total_erro = 0
    total_valor_importado = 0
    total_pagas = 0
    total_em_aberto = 0

    # Formato: Dia_Nov, Descricao_Nov, Valor_Nov, Status_Nov, Dia_Dez, Descricao_Dez, Valor_Dez, Status_Dez
    # Índices: 0, 1, 2, 3, 4, 5, 6, 7

    print("📅 IMPORTANDO DESPESAS DE NOVEMBRO E DEZEMBRO/2025...\n")

    for linha in linhas_dados:
        if len(linha) < 4:
            continue

        # Processar Novembro (colunas 0, 1, 2, 3)
        dia_nov = linha[0].strip() if len(linha) > 0 and linha[0].strip() else None
        desc_nov = linha[1].strip() if len(linha) > 1 and linha[1].strip() else None
        valor_nov_str = linha[2].strip() if len(linha) > 2 and linha[2].strip() else None
        status_nov = linha[3].strip() if len(linha) > 3 and linha[3].strip() else None

        if dia_nov and desc_nov and valor_nov_str and status_nov:
            valor_nov = limpar_valor(valor_nov_str)
            descricao_nov = normalizar_descricao(desc_nov)

            if valor_nov and valor_nov > 0 and descricao_nov:
                try:
                    dia = int(dia_nov)
                    data = f"2025-11-{dia:02d}"
                    paid = status_nov.lower() == "pago"

                    resultado = criar_despesa(data, valor_nov, descricao_nov, paid, dry_run)
                    total_despesas += 1
                    total_valor_importado += valor_nov

                    if paid:
                        total_pagas += 1
                    else:
                        total_em_aberto += 1

                    if resultado["status"] == "success" or resultado["status"] == "dry_run":
                        total_sucesso += 1
                    else:
                        total_erro += 1
                except ValueError:
                    pass

        # Processar Dezembro (colunas 4, 5, 6, 7)
        dia_dez = linha[4].strip() if len(linha) > 4 and linha[4].strip() else None
        desc_dez = linha[5].strip() if len(linha) > 5 and linha[5].strip() else None
        valor_dez_str = linha[6].strip() if len(linha) > 6 and linha[6].strip() else None
        status_dez = linha[7].strip() if len(linha) > 7 and linha[7].strip() else None

        if dia_dez and desc_dez and valor_dez_str and status_dez:
            valor_dez = limpar_valor(valor_dez_str)
            descricao_dez = normalizar_descricao(desc_dez)

            if valor_dez and valor_dez > 0 and descricao_dez:
                try:
                    dia = int(dia_dez)
                    data = f"2025-12-{dia:02d}"
                    paid = status_dez.lower() == "pago"

                    resultado = criar_despesa(data, valor_dez, descricao_dez, paid, dry_run)
                    total_despesas += 1
                    total_valor_importado += valor_dez

                    if paid:
                        total_pagas += 1
                    else:
                        total_em_aberto += 1

                    if resultado["status"] == "success" or resultado["status"] == "dry_run":
                        total_sucesso += 1
                    else:
                        total_erro += 1
                except ValueError:
                    pass

    # Resumo
    print(f"\n{'='*80}")
    print(f"RESUMO:")
    print(f"  Total processado: {total_despesas}")
    print(f"  Sucesso: {total_sucesso}")
    print(f"  Erros: {total_erro}")
    print(f"  Pagas: {total_pagas}")
    print(f"  Em aberto: {total_em_aberto}")
    print(f"  Valor total importado: R$ {total_valor_importado:,.2f}")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    import sys

    # Caminho do arquivo CSV
    arquivo_csv = "contas-2025.csv"

    # Por padrão, executa em modo dry_run
    dry_run = True

    # Se passar "execute" como argumento, executa de verdade
    if len(sys.argv) > 1 and sys.argv[1] == "execute":
        dry_run = False
        confirmacao = input("⚠️  ATENÇÃO: Você está prestes a executar o import REAL. Confirma? (sim/não): ")
        if confirmacao.lower() != "sim":
            print("Operação cancelada.")
            sys.exit(0)

    processar_csv(arquivo_csv, dry_run)

    if dry_run:
        print("\n💡 Para executar de verdade, rode: python3 import_despesas_2025.py execute")
