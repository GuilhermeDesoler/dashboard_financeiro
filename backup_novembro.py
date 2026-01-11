import requests
import json
from datetime import datetime

# Configurações da API
API_BASE_URL = "http://localhost:5000"
API_ENDPOINT = f"{API_BASE_URL}/api/financial-entries"

# Token de autenticação
AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYzkxMzY2YmUtMDIzMC00OTJkLTk4OTUtMTI2NjhlYTZjYzA0IiwiZW1haWwiOiJzdXBlckB0ZXN0ZS5jb20iLCJuYW1lIjoiU3VwZXIgQWRtaW4iLCJjb21wYW55X2lkIjpudWxsLCJyb2xlcyI6W10sImZlYXR1cmVzIjpbXSwiaXNfc3VwZXJfYWRtaW4iOnRydWUsImV4cCI6MTc2ODE4Nzg5MCwiaWF0IjoxNzY4MTAxNDkwfQ.X1NYrmFMk3WSy8sC29YgygxoQb8VZEodim3p3nangyk"

def backup_lancamentos(start_date, end_date):
    """Faz backup de todos os lançamentos de um período"""

    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }

    print("="*80)
    print(f"BACKUP DE LANÇAMENTOS DE {start_date} A {end_date}")
    print("="*80)

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
            print("\n⚠️  Nenhum lançamento para fazer backup!")
            return

        # Gera nome do arquivo com timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"backup_lancamentos_novembro_{timestamp}.json"

        # Salva o backup
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(lancamentos, f, ensure_ascii=False, indent=2)

        print(f"\n✅ Backup salvo em: {filename}")

        # Mostra resumo
        total_valor = sum(lanc['value'] for lanc in lancamentos)
        print(f"\n📋 Resumo do backup:")
        print(f"  Total de lançamentos: {len(lancamentos)}")
        print(f"  Valor total: R$ {total_valor:,.2f}")

        # Agrupa por modalidade
        modalidades = {}
        for lanc in lancamentos:
            mod = lanc.get('modality_name', 'Sem modalidade')
            if mod not in modalidades:
                modalidades[mod] = {'count': 0, 'value': 0}
            modalidades[mod]['count'] += 1
            modalidades[mod]['value'] += lanc['value']

        print(f"\n📊 Por modalidade:")
        for mod, data in sorted(modalidades.items(), key=lambda x: x[1]['value'], reverse=True):
            print(f"  {mod:<40} | {data['count']:>3} lançamentos | R$ {data['value']:>12,.2f}")

        print("\n" + "="*80)

    except Exception as e:
        print(f"\n❌ Erro ao fazer backup: {str(e)}")


if __name__ == "__main__":
    # Período do backup
    start_date = "2025-11-01"
    end_date = "2025-11-30"

    backup_lancamentos(start_date, end_date)
