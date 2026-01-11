import requests

# Configurações da API
API_BASE_URL = "http://localhost:5000"
API_ENDPOINT = f"{API_BASE_URL}/api/financial-entries"

# Token de autenticação
AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYzkxMzY2YmUtMDIzMC00OTJkLTk4OTUtMTI2NjhlYTZjYzA0IiwiZW1haWwiOiJzdXBlckB0ZXN0ZS5jb20iLCJuYW1lIjoiU3VwZXIgQWRtaW4iLCJjb21wYW55X2lkIjpudWxsLCJyb2xlcyI6W10sImZlYXR1cmVzIjpbXSwiaXNfc3VwZXJfYWRtaW4iOnRydWUsImV4cCI6MTc2ODE4Nzg5MCwiaWF0IjoxNzY4MTAxNDkwfQ.X1NYrmFMk3WSy8sC29YgygxoQb8VZEodim3p3nangyk"

def deletar_lancamentos_periodo(start_date, end_date, dry_run=True):
    """Deleta todos os lançamentos de um período"""

    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }

    print("="*80)
    print(f"DELETANDO LANÇAMENTOS DE {start_date} A {end_date}")
    print(f"MODO: {'DRY RUN (simulação)' if dry_run else 'EXECUÇÃO REAL'}")
    print("="*80)

    # Busca todos os lançamentos do período
    try:
        response = requests.get(
            API_ENDPOINT,
            params={"start_date": start_date, "end_date": end_date},
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        lancamentos = response.json()

        print(f"\n📊 Encontrados {len(lancamentos)} lançamentos no período")

        if len(lancamentos) == 0:
            print("\n✅ Nenhum lançamento para deletar!")
            return

        # Mostra preview dos primeiros 10
        print("\n📋 Preview dos primeiros 10 lançamentos:")
        for i, lanc in enumerate(lancamentos[:10], 1):
            print(f"  {i}. {lanc['date']} | R$ {lanc['value']:,.2f} | {lanc['modality_name']} | ID: {lanc['id']}")

        if len(lancamentos) > 10:
            print(f"  ... e mais {len(lancamentos) - 10} lançamentos")

        if dry_run:
            print(f"\n🔵 DRY RUN: {len(lancamentos)} lançamentos SERIAM deletados")
            return

        # Deleta cada lançamento
        deletados = 0
        erros = 0

        print(f"\n🗑️  Deletando {len(lancamentos)} lançamentos...")

        for i, lanc in enumerate(lancamentos, 1):
            try:
                response = requests.delete(
                    f"{API_ENDPOINT}/{lanc['id']}",
                    headers=headers,
                    timeout=30
                )
                response.raise_for_status()
                deletados += 1

                if i % 50 == 0:
                    print(f"  Progresso: {i}/{len(lancamentos)} ({(i/len(lancamentos)*100):.1f}%)")

            except Exception as e:
                erros += 1
                print(f"  ❌ Erro ao deletar {lanc['id']}: {str(e)}")

        print("\n" + "="*80)
        print("RESUMO:")
        print(f"  Deletados: {deletados}")
        print(f"  Erros: {erros}")
        print("="*80)

    except Exception as e:
        print(f"\n❌ Erro ao buscar lançamentos: {str(e)}")


if __name__ == "__main__":
    import sys

    # Período a deletar
    start_date = "2025-11-01"
    end_date = "2025-11-30"

    # Por padrão, executa em modo dry_run
    dry_run = True

    # Se passar "execute" como argumento, executa de verdade
    if len(sys.argv) > 1 and sys.argv[1] == "execute":
        dry_run = False
        print(f"\n⚠️  ATENÇÃO: Você está prestes a DELETAR todos os lançamentos de {start_date} a {end_date}")
        confirmacao = input("Digite 'DELETAR' para confirmar: ")
        if confirmacao != "DELETAR":
            print("Operação cancelada.")
            sys.exit(0)

    deletar_lancamentos_periodo(start_date, end_date, dry_run)

    if dry_run:
        print("\n💡 Para executar de verdade, rode: python3 deletar_lancamentos_periodo.py execute")
