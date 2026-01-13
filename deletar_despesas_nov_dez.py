import requests

# Configurações da API
API_BASE_URL = "http://localhost:5000"
API_ENDPOINT = f"{API_BASE_URL}/api/accounts"

# Token de autenticação
AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYzkxMzY2YmUtMDIzMC00OTJkLTk4OTUtMTI2NjhlYTZjYzA0IiwiZW1haWwiOiJzdXBlckB0ZXN0ZS5jb20iLCJuYW1lIjoiU3VwZXIgQWRtaW4iLCJjb21wYW55X2lkIjpudWxsLCJyb2xlcyI6W10sImZlYXR1cmVzIjpbXSwiaXNfc3VwZXJfYWRtaW4iOnRydWUsImV4cCI6MTc2ODE4Nzg5MCwiaWF0IjoxNzY4MTAxNDkwfQ.X1NYrmFMk3WSy8sC29YgygxoQb8VZEodim3p3nangyk"

def deletar_despesas_periodo(start_date, end_date, dry_run=True):
    """Deleta todas as despesas (type=payment) de um período"""

    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }

    print("="*80)
    print(f"DELETANDO DESPESAS DE {start_date} A {end_date}")
    print(f"MODO: {'DRY RUN (simulação)' if dry_run else 'EXECUÇÃO REAL'}")
    print("="*80)

    try:
        response = requests.get(
            API_ENDPOINT,
            params={"start_date": start_date, "end_date": end_date},
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        all_accounts = response.json()

        # Filtrar apenas despesas (type=payment)
        despesas = [acc for acc in all_accounts if acc.get('type') == 'payment']

        print(f"\n📊 Encontradas {len(despesas)} despesas no período")

        if len(despesas) == 0:
            print("\n✅ Nenhuma despesa para deletar!")
            return

        # Mostra preview dos primeiros 10
        print("\n📋 Preview dos primeiros 10 despesas:")
        for i, desp in enumerate(despesas[:10], 1):
            print(f"  {i}. {desp['date']} | R$ {desp['value']:,.2f} | {desp['description']} | ID: {desp['id']}")

        if len(despesas) > 10:
            print(f"  ... e mais {len(despesas) - 10} despesas")

        if dry_run:
            print(f"\n🔵 DRY RUN: {len(despesas)} despesas SERIAM deletadas")
            return

        # Deleta cada despesa
        deletados = 0
        erros = 0

        print(f"\n🗑️  Deletando {len(despesas)} despesas...")

        for i, desp in enumerate(despesas, 1):
            try:
                response = requests.delete(
                    f"{API_ENDPOINT}/{desp['id']}",
                    headers=headers,
                    timeout=30
                )
                response.raise_for_status()
                deletados += 1

                if i % 10 == 0:
                    print(f"  Progresso: {i}/{len(despesas)} ({(i/len(despesas)*100):.1f}%)")

            except Exception as e:
                erros += 1
                print(f"  ❌ Erro ao deletar {desp['id']}: {str(e)}")

        print("\n" + "="*80)
        print("RESUMO:")
        print(f"  Deletados: {deletados}")
        print(f"  Erros: {erros}")
        print("="*80)

    except Exception as e:
        print(f"\n❌ Erro ao buscar despesas: {str(e)}")


if __name__ == "__main__":
    import sys

    # Período a deletar
    start_date = "2025-11-01"
    end_date = "2025-12-31"

    # Por padrão, executa em modo dry_run
    dry_run = True

    # Se passar "execute" como argumento, executa de verdade
    if len(sys.argv) > 1 and sys.argv[1] == "execute":
        dry_run = False
        print(f"\n⚠️  ATENÇÃO: Você está prestes a DELETAR todas as despesas de {start_date} a {end_date}")
        confirmacao = input("Digite 'DELETAR' para confirmar: ")
        if confirmacao != "DELETAR":
            print("Operação cancelada.")
            sys.exit(0)

    deletar_despesas_periodo(start_date, end_date, dry_run)

    if dry_run:
        print("\n💡 Para executar de verdade, rode: python3 deletar_despesas_nov_dez.py execute")
