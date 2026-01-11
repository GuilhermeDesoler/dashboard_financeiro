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


def criar_boleto(data, valor, dry_run=True):
    """Cria um boleto via API"""

    # Prepara o payload
    payload = {
        "value": valor,
        "date": data,
        "description": "Boleto",
        "type": "boleto"
    }

    if dry_run:
        print(f"  🔵 DRY RUN: {data} - R$ {valor:,.2f} - Boleto")
        return {"status": "dry_run", "payload": payload}

    # Faz a requisição
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(API_ENDPOINT, json=payload, headers=headers)

        if response.status_code in [200, 201]:
            print(f"  ✅ SUCESSO: {data} - R$ {valor:,.2f} - Boleto")
            return {"status": "success", "response": response.json()}
        else:
            print(f"  ❌ ERRO: {data} - R$ {valor:,.2f} - Boleto")
            print(f"     Status: {response.status_code}")
            print(f"     Resposta: {response.text}")
            return {"status": "error", "status_code": response.status_code, "response": response.text}

    except Exception as e:
        print(f"  ❌ EXCEÇÃO: {data} - R$ {valor:,.2f} - Boleto")
        print(f"     Erro: {str(e)}")
        return {"status": "exception", "error": str(e)}


def processar_csv(arquivo_csv, dry_run=True):
    """Processa o arquivo CSV e cria os boletos"""

    print(f"\n{'='*80}")
    print(f"PROCESSANDO ARQUIVO: {arquivo_csv}")
    print(f"MODO: {'DRY RUN (simulação)' if dry_run else 'EXECUÇÃO REAL'}")
    print(f"{'='*80}\n")

    with open(arquivo_csv, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        linhas = list(reader)

    # A primeira linha contém os nomes dos meses
    header = linhas[0]

    # A segunda linha contém os totais (ignorar)
    # A partir da terceira linha, temos os dados
    linhas_dados = linhas[2:]

    total_boletos = 0
    total_sucesso = 0
    total_erro = 0
    total_valor_importado = 0

    # Identificar colunas (Novembro = colunas 0 e 1, Dezembro = colunas 2 e 3)
    # Formato: Dia_Nov, Valor_Nov, Dia_Dez, Valor_Dez

    print("📅 IMPORTANDO BOLETOS DE NOVEMBRO/2025...\n")

    for linha in linhas_dados:
        if len(linha) < 2:
            continue

        # Processar Novembro (colunas 0 e 1)
        dia_nov = linha[0].strip() if len(linha) > 0 and linha[0].strip() else None
        valor_nov_str = linha[1].strip() if len(linha) > 1 and linha[1].strip() else None

        if dia_nov and valor_nov_str:
            valor_nov = limpar_valor(valor_nov_str)
            if valor_nov and valor_nov > 0:
                try:
                    dia = int(dia_nov)
                    data = f"2025-11-{dia:02d}"
                    resultado = criar_boleto(data, valor_nov, dry_run)
                    total_boletos += 1
                    total_valor_importado += valor_nov

                    if resultado["status"] == "success" or resultado["status"] == "dry_run":
                        total_sucesso += 1
                    else:
                        total_erro += 1
                except ValueError:
                    pass

        # Processar Dezembro (colunas 2 e 3)
        dia_dez = linha[2].strip() if len(linha) > 2 and linha[2].strip() else None
        valor_dez_str = linha[3].strip() if len(linha) > 3 and linha[3].strip() else None

        if dia_dez and valor_dez_str:
            valor_dez = limpar_valor(valor_dez_str)
            if valor_dez and valor_dez > 0:
                try:
                    dia = int(dia_dez)
                    data = f"2025-12-{dia:02d}"
                    resultado = criar_boleto(data, valor_dez, dry_run)
                    total_boletos += 1
                    total_valor_importado += valor_dez

                    if resultado["status"] == "success" or resultado["status"] == "dry_run":
                        total_sucesso += 1
                    else:
                        total_erro += 1
                except ValueError:
                    pass

    # Resumo
    print(f"\n{'='*80}")
    print(f"RESUMO:")
    print(f"  Total processado: {total_boletos}")
    print(f"  Sucesso: {total_sucesso}")
    print(f"  Erros: {total_erro}")
    print(f"  Valor total importado: R$ {total_valor_importado:,.2f}")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    import sys

    # Caminho do arquivo CSV
    arquivo_csv = "boletos-2025.csv"

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
        print("\n💡 Para executar de verdade, rode: python3 import_boletos_2025.py execute")
