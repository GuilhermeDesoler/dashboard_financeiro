import requests
from typing import Optional, Dict, Any
from config import Environment


class HTTPClient:
    def __init__(self):
        self.env = Environment()
        self.base_url = self.env.base_url.rstrip("/")
        self.timeout = 30
        self._auth_token: Optional[str] = None

    def set_auth_token(self, token: Optional[str]):
        """Set the authentication token for all requests"""
        self._auth_token = token

    def _get_headers(self) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self._auth_token:
            headers["Authorization"] = f"Bearer {self._auth_token}"
        return headers

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
        try:
            response = requests.post(
                url, json=data, headers=self._get_headers(), timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            try:
                error_detail = response.json()
                raise Exception(f"{e} - Detalhes: {error_detail}") from e
            except Exception:
                raise Exception(f"{e} - Response: {response.text[:500]}") from e

    def put(self, endpoint: str, data: Dict[str, Any]) -> Dict:
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.put(
                url, json=data, headers=self._get_headers(), timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            try:
                error_detail = response.json()
                raise Exception(f"{e} - Detalhes: {error_detail}") from e
            except Exception:
                raise Exception(f"{e} - Response: {response.text[:500]}") from e

    def patch(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict:
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.patch(
                url, json=data, headers=self._get_headers(), timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            try:
                error_detail = response.json()
                raise Exception(f"{e} - Detalhes: {error_detail}") from e
            except Exception:
                raise Exception(f"{e} - Response: {response.text[:500]}") from e

    def delete(self, endpoint: str) -> bool:
        url = f"{self.base_url}{endpoint}"
        response = requests.delete(url, headers=self._get_headers(), timeout=self.timeout)
        response.raise_for_status()
        return response.status_code == 204 or response.status_code == 200
