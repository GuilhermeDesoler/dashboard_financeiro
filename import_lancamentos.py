import csv
import requests
from datetime import datetime
import re

# Configurações da API
API_BASE_URL = "http://localhost:5000"  # Ajuste conforme necessário
API_ENDPOINT = f"{API_BASE_URL}/api/financial-entries"

# Token de autenticação (você precisa ajustar isso)
AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYzkxMzY2YmUtMDIzMC00OTJkLTk4OTUtMTI2NjhlYTZjYzA0IiwiZW1haWwiOiJzdXBlckB0ZXN0ZS5jb20iLCJuYW1lIjoiU3VwZXIgQWRtaW4iLCJjb21wYW55X2lkIjpudWxsLCJyb2xlcyI6W10sImZlYXR1cmVzIjpbXSwiaXNfc3VwZXJfYWRtaW4iOnRydWUsImV4cCI6MTc2ODE4Nzg5MCwiaWF0IjoxNzY4MTAxNDkwfQ.X1NYrmFMk3WSy8sC29YgygxoQb8VZEodim3p3nangyk"

# Mapeamento de modalidades
MODALIDADES = {
    "Dinheiro": {
        "id": "d7c886f7-3768-45a9-a522-bf1a377b9828",
        "is_credit_payment": False
    },
    "Pix Sicredi": {
        "id": "43ebc7c3-bf22-481b-a59f-0379669eb355",
        "is_credit_payment": False
    },
    "Pix Sicoob": {
        "id": "702ee6e4-ce26-4202-b751-97f88390ae19",
        "is_credit_payment": False
    },
    "Débito Sicredi": {
        "id": "a611381f-e26e-456d-998d-c25ab4d16b08",
        "is_credit_payment": False
    },
    "Debito Sicoob": {
        "id": "a611381f-e26e-456d-998d-c25ab4d16b08",  # Ajustar se for diferente
        "is_credit_payment": False
    },
    "Recebimento Crediario": {
        "id": "654050e3-75ae-4438-82b2-b8c6ff497e0c",  # Você precisa fornecer o ID desta modalidade
        "is_credit_payment": True
    },
    "Crédito Av Sicredi": {
        "id": "26646ee2-09a1-4a1c-9aee-74ff6ea4fcce",
        "is_credit_payment": False
    },
    "Parcelado 2 a 4 Sicredi": {
        "id": "c32cde4a-e41b-46bb-b940-fb42a506d94c",
        "is_credit_payment": False
    },
    "Parcelado 5 a 6 Sicredi": {
        "id": "065a0aba-f327-4687-b575-6d4c6c12f5df",
        "is_credit_payment": False
    },
    "Parcelado 5 a 6 Sicoob": {
        "id": "6e6c3e3c-463f-474c-95d4-5355585facc9",
        "is_credit_payment": False
    },
    "BonusCred": {
        "id": "32a3eeaa-cfec-48d0-b6b4-69504b7a6dce",
        "is_credit_payment": False
    }
}


def limpar_valor(valor_str):
    """Converte string de valor brasileiro para float"""
    if not valor_str or valor_str.strip() == "":
        return None

    # Remove "R$" e espaços
    valor_str = valor_str.replace("R$", "").strip()
    # Remove pontos de milhar
    valor_str = valor_str.replace(".", "")
    # Substitui vírgula por ponto decimal
    valor_str = valor_str.replace(",", ".")

    try:
        return float(valor_str)
    except ValueError:
        return None


def normalizar_modalidade(modalidade_str):
    """Normaliza o nome da modalidade removendo caracteres especiais"""
    if not modalidade_str:
        return None

    # Remove caracteres especiais de encoding
    modalidade_str = modalidade_str.replace("Ã©", "é")
    modalidade_str = modalidade_str.replace("Ã¡", "á")
    modalidade_str = modalidade_str.replace("Ã­", "í")
    modalidade_str = modalidade_str.replace("Ã³", "ó")

    return modalidade_str.strip()


def converter_data(data_str):
    """Converte string de data DD/MM/YYYY para formato YYYY-MM-DD"""
    if not data_str or data_str.strip() == "":
        return None

    try:
        data_obj = datetime.strptime(data_str, "%d/%m/%Y")
        return data_obj.strftime("%Y-%m-%d")
    except ValueError:
        return None


def criar_lancamento(data, valor, modalidade_nome, dry_run=True):
    """Cria um lançamento via API"""

    # Normaliza o nome da modalidade
    modalidade_nome = normalizar_modalidade(modalidade_nome)

    # Ignora modalidades do tipo Crediário
    if "Crediário" in modalidade_nome or "CrediÃ¡rio" in modalidade_nome:
        print(f"  ⏭️  IGNORADO (Crediário): {data} - {valor} - {modalidade_nome}")
        return {"status": "ignored", "reason": "credario"}

    # Busca a modalidade no mapeamento
    modalidade_info = MODALIDADES.get(modalidade_nome)

    if not modalidade_info:
        print(f"  ⚠️  MODALIDADE NÃO ENCONTRADA: {modalidade_nome}")
        return {"status": "error", "reason": "modalidade_nao_encontrada"}

    # Prepara o payload
    payload = {
        "value": valor,
        "date": data,
        "modality_id": modalidade_info["id"]
    }

    # Adiciona is_credit_payment se for Recebimento Crediario
    if modalidade_info["is_credit_payment"]:
        payload["is_credit_payment"] = True

    if dry_run:
        print(f"  🔵 DRY RUN: {data} - R$ {valor:,.2f} - {modalidade_nome}")
        print(f"     Payload: {payload}")
        return {"status": "dry_run", "payload": payload}

    # Faz a requisição
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(API_ENDPOINT, json=payload, headers=headers)

        if response.status_code in [200, 201]:
            print(f"  ✅ SUCESSO: {data} - R$ {valor:,.2f} - {modalidade_nome}")
            return {"status": "success", "response": response.json()}
        else:
            print(f"  ❌ ERRO: {data} - {valor} - {modalidade_nome}")
            print(f"     Status: {response.status_code}")
            print(f"     Resposta: {response.text}")
            return {"status": "error", "status_code": response.status_code, "response": response.text}

    except Exception as e:
        print(f"  ❌ EXCEÇÃO: {data} - {valor} - {modalidade_nome}")
        print(f"     Erro: {str(e)}")
        return {"status": "exception", "error": str(e)}


def processar_csv(arquivo_csv, dry_run=True):
    """Processa o arquivo CSV e cria os lançamentos"""

    print(f"\n{'='*80}")
    print(f"PROCESSANDO ARQUIVO: {arquivo_csv}")
    print(f"MODO: {'DRY RUN (simulação)' if dry_run else 'EXECUÇÃO REAL'}")
    print(f"{'='*80}\n")

    with open(arquivo_csv, 'r', encoding='utf-8') as file:
        # Lê o arquivo como texto
        linhas = file.readlines()

        # A primeira linha contém as datas e "Modalidade"
        header = linhas[0].strip().split(',')

        # Extrai as datas (posições pares: 0, 2, 4, 6...)
        datas = []
        for i in range(0, len(header), 2):
            data_str = header[i]
            data_formatada = converter_data(data_str)
            if data_formatada:
                datas.append(data_formatada)

        print(f"📅 Encontradas {len(datas)} datas\n")

        # Pula as duas primeiras linhas (header e linha vazia)
        linhas_dados = linhas[2:]

        total_lancamentos = 0
        total_sucesso = 0
        total_erro = 0
        total_ignorado = 0

        # Processa cada linha de dados
        for idx, linha in enumerate(linhas_dados):
            valores = linha.strip().split(',')

            if len(valores) < 2:
                continue

            # Processa cada par valor/modalidade
            for i in range(0, min(len(valores), len(datas) * 2), 2):
                data_idx = i // 2

                if data_idx >= len(datas):
                    break

                valor_str = valores[i] if i < len(valores) else ""
                modalidade_str = valores[i + 1] if i + 1 < len(valores) else ""

                valor = limpar_valor(valor_str)
                modalidade = normalizar_modalidade(modalidade_str)

                # Só processa se tiver valor e modalidade
                if valor and modalidade:
                    data = datas[data_idx]

                    resultado = criar_lancamento(data, valor, modalidade, dry_run)
                    total_lancamentos += 1

                    if resultado["status"] == "success" or resultado["status"] == "dry_run":
                        total_sucesso += 1
                    elif resultado["status"] == "ignored":
                        total_ignorado += 1
                    else:
                        total_erro += 1

        # Resumo
        print(f"\n{'='*80}")
        print(f"RESUMO:")
        print(f"  Total processado: {total_lancamentos}")
        print(f"  Sucesso: {total_sucesso}")
        print(f"  Ignorados (Crediário): {total_ignorado}")
        print(f"  Erros: {total_erro}")
        print(f"{'='*80}\n")


if __name__ == "__main__":
    import sys

    # Caminho do arquivo CSV
    arquivo_csv = "Planilha sem título - Página1.csv"

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
        print("\n💡 Para executar de verdade, rode: python import_lancamentos.py execute")
