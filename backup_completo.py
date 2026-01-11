import requests
import json
from datetime import datetime
from collections import defaultdict

# Configurações da API
API_BASE_URL = "http://localhost:5000"
API_ENDPOINT = f"{API_BASE_URL}/api/financial-entries"

# Token de autenticação
AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYzkxMzY2YmUtMDIzMC00OTJkLTk4OTUtMTI2NjhlYTZjYzA0IiwiZW1haWwiOiJzdXBlckB0ZXN0ZS5jb20iLCJuYW1lIjoiU3VwZXIgQWRtaW4iLCJjb21wYW55X2lkIjpudWxsLCJyb2xlcyI6W10sImZlYXR1cmVzIjpbXSwiaXNfc3VwZXJfYWRtaW4iOnRydWUsImV4cCI6MTc2ODE4Nzg5MCwiaWF0IjoxNzY4MTAxNDkwfQ.X1NYrmFMk3WSy8sC29YgygxoQb8VZEodim3p3nangyk"

def backup_completo():
    """Faz backup completo de todos os lançamentos"""

    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }

    print("="*80)
    print("BACKUP COMPLETO DE TODOS OS LANÇAMENTOS")
    print("="*80)

    try:
        # Busca todos os lançamentos (sem filtro de data)
        response = requests.get(
            API_ENDPOINT,
            headers=headers,
            timeout=60
        )
        response.raise_for_status()
        lancamentos = response.json()

        print(f"\n📊 Encontrados {len(lancamentos)} lançamentos no total")

        if len(lancamentos) == 0:
            print("\n⚠️  Nenhum lançamento para fazer backup!")
            return

        # Gera nome do arquivo com timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"backup_completo_{timestamp}.json"

        # Salva o backup
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(lancamentos, f, ensure_ascii=False, indent=2)

        print(f"\n✅ Backup salvo em: {filename}")

        # Mostra resumo
        total_valor = sum(lanc['value'] for lanc in lancamentos)
        print(f"\n📋 Resumo do backup:")
        print(f"  Total de lançamentos: {len(lancamentos)}")
        print(f"  Valor total: R$ {total_valor:,.2f}")

        # Agrupa por mês/ano
        por_mes = defaultdict(lambda: {'count': 0, 'value': 0})
        for lanc in lancamentos:
            data = lanc.get('date', '')
            if data:
                mes_ano = data[:7]  # YYYY-MM
                por_mes[mes_ano]['count'] += 1
                por_mes[mes_ano]['value'] += lanc['value']

        print(f"\n📅 Por mês:")
        for mes in sorted(por_mes.keys()):
            data = por_mes[mes]
            print(f"  {mes} | {data['count']:>4} lançamentos | R$ {data['value']:>12,.2f}")

        # Agrupa por modalidade
        modalidades = defaultdict(lambda: {'count': 0, 'value': 0})
        for lanc in lancamentos:
            mod = lanc.get('modality_name', 'Sem modalidade')
            modalidades[mod]['count'] += 1
            modalidades[mod]['value'] += lanc['value']

        print(f"\n📊 Por modalidade (top 15):")
        top_modalidades = sorted(modalidades.items(), key=lambda x: x[1]['value'], reverse=True)[:15]
        for mod, data in top_modalidades:
            print(f"  {mod:<40} | {data['count']:>4} lançamentos | R$ {data['value']:>12,.2f}")

        print("\n" + "="*80)
        print(f"✅ Backup completo finalizado: {filename}")
        print("="*80)

    except Exception as e:
        print(f"\n❌ Erro ao fazer backup: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    backup_completo()
