import requests

# Configurações da API
API_BASE_URL = "http://localhost:5000"
API_ENDPOINT = f"{API_BASE_URL}/api/accounts"

# Token de autenticação
AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYzkxMzY2YmUtMDIzMC00OTJkLTk4OTUtMTI2NjhlYTZjYzA0IiwiZW1haWwiOiJzdXBlckB0ZXN0ZS5jb20iLCJuYW1lIjoiU3VwZXIgQWRtaW4iLCJjb21wYW55X2lkIjpudWxsLCJyb2xlcyI6W10sImZlYXR1cmVzIjpbXSwiaXNfc3VwZXJfYWRtaW4iOnRydWUsImV4cCI6MTc2ODE4Nzg5MCwiaWF0IjoxNzY4MTAxNDkwfQ.X1NYrmFMk3WSy8sC29YgygxoQb8VZEodim3p3nangyk"

# Proventos a importar
proventos = [
    {"descricao": "Provento Ana Marli", "valor": 4350.00},
    {"descricao": "Provento Ana Laura", "valor": 1500.00},
    {"descricao": "Provento Isa", "valor": 3500.00},
]

def criar_despesa(data, valor, descricao, paid, dry_run=True):
    """Cria uma despesa via API"""

    payload = {
        "value": valor,
        "date": data,
        "description": descricao,
        "type": "payment",
        "paid": paid
    }

    if dry_run:
        print(f"  🔵 DRY RUN: {data} - R$ {valor:,.2f} - {descricao} - ✅ Pago")
        return {"status": "dry_run", "payload": payload}

    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(API_ENDPOINT, json=payload, headers=headers)

        if response.status_code in [200, 201]:
            print(f"  ✅ SUCESSO: {data} - R$ {valor:,.2f} - {descricao} - ✅ Pago")
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


if __name__ == "__main__":
    import sys

    dry_run = True

    if len(sys.argv) > 1 and sys.argv[1] == "execute":
        dry_run = False
        confirmacao = input("⚠️  ATENÇÃO: Você está prestes a executar o import REAL dos 3 proventos. Confirma? (sim/não): ")
        if confirmacao.lower() != "sim":
            print("Operação cancelada.")
            sys.exit(0)

    print("="*80)
    print("IMPORTANDO 3 PROVENTOS DE NOVEMBRO (DIA 25/11/2025)")
    print(f"MODO: {'DRY RUN (simulação)' if dry_run else 'EXECUÇÃO REAL'}")
    print("="*80)
    print()

    total_sucesso = 0
    total_erro = 0
    total_valor = 0

    for provento in proventos:
        resultado = criar_despesa(
            data="2025-11-25",
            valor=provento["valor"],
            descricao=provento["descricao"],
            paid=True,
            dry_run=dry_run
        )

        if resultado["status"] == "success" or resultado["status"] == "dry_run":
            total_sucesso += 1
            total_valor += provento["valor"]
        else:
            total_erro += 1

    print()
    print("="*80)
    print("RESUMO:")
    print(f"  Sucesso: {total_sucesso}")
    print(f"  Erros: {total_erro}")
    print(f"  Valor total: R$ {total_valor:,.2f}")
    print("="*80)

    if dry_run:
        print("\n💡 Para executar de verdade, rode: python3 import_proventos_novembro.py execute")
