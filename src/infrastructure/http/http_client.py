import requests
from typing import Optional, Dict, Any
from config import Environment


class HTTPClient:
    def __init__(self):
        self.env = Environment()
        self.base_url = self.env.base_url.rstrip("/")
        self.timeout = 30

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict:
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(
                url, params=params, headers=self._get_headers(), timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            # Tenta pegar o corpo da resposta para debug
            try:
                error_detail = response.json()
                raise Exception(f"{e} - Detalhes: {error_detail}")
            except:
                raise Exception(f"{e} - Response: {response.text[:200]}")
        except Exception as e:
            raise Exception(f"Erro ao fazer requisição GET para {url}: {str(e)}")

    def post(self, endpoint: str, data: Dict[str, Any]) -> Dict:
        url = f"{self.base_url}{endpoint}"
        response = requests.post(
            url, json=data, headers=self._get_headers(), timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def put(self, endpoint: str, data: Dict[str, Any]) -> Dict:
        url = f"{self.base_url}{endpoint}"
        response = requests.put(
            url, json=data, headers=self._get_headers(), timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def patch(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict:
        url = f"{self.base_url}{endpoint}"
        response = requests.patch(
            url, json=data, headers=self._get_headers(), timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def delete(self, endpoint: str) -> bool:
        url = f"{self.base_url}{endpoint}"
        response = requests.delete(url, headers=self._get_headers(), timeout=self.timeout)
        response.raise_for_status()
        return response.status_code == 204 or response.status_code == 200
