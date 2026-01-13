import requests
import json
from datetime import datetime

# Configurações da API
API_BASE_URL = "http://localhost:5000"
API_ENDPOINT = f"{API_BASE_URL}/api/financial-entries"

# Token de autenticação
AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYzkxMzY2YmUtMDIzMC00OTJkLTk4OTUtMTI2NjhlYTZjYzA0IiwiZW1haWwiOiJzdXBlckB0ZXN0ZS5jb20iLCJuYW1lIjoiU3VwZXIgQWRtaW4iLCJjb21wYW55X2lkIjpudWxsLCJyb2xlcyI6W10sImZlYXR1cmVzIjpbXSwiaXNfc3VwZXJfYWRtaW4iOnRydWUsImV4cCI6MTc2ODE4Nzg5MCwiaWF0IjoxNzY4MTAxNDkwfQ.X1NYrmFMk3WSy8sC29YgygxoQb8VZEodim3p3nangyk"

def fazer_backup():
    """Faz backup de todos os lançamentos atuais"""

    print("="*80)
    print("FAZENDO BACKUP DOS LANÇAMENTOS")
    print("="*80)

    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        # Busca todos os lançamentos
        response = requests.get(API_ENDPOINT, headers=headers, timeout=30)
        response.raise_for_status()

        lancamentos = response.json()

        # Nome do arquivo de backup
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"backup_lancamentos_{timestamp}.json"

        # Salva no arquivo
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(lancamentos, f, indent=2, ensure_ascii=False)

        print(f"\n✅ Backup realizado com sucesso!")
        print(f"📁 Arquivo: {backup_file}")
        print(f"📊 Total de lançamentos salvos: {len(lancamentos)}")
        print("="*80)

        return backup_file

    except Exception as e:
        print(f"\n❌ Erro ao fazer backup: {str(e)}")
        return None

if __name__ == "__main__":
    fazer_backup()
