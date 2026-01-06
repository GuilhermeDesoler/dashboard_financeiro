from typing import List
from domain.entities.bank_limit import BankLimit
from domain.repositories.bank_limit_repository import BankLimitRepository
from infrastructure.http import HTTPClient


class BankLimitAPIRepository(BankLimitRepository):
    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client
        self.base_endpoint = "/api/bank-limits"

    def create(
        self,
        bank_name: str,
        rotativo_available: float = 0.0,
        rotativo_used: float = 0.0,
        cheque_available: float = 0.0,
        cheque_used: float = 0.0,
    ) -> BankLimit:
        data = {
            "bank_name": bank_name,
            "rotativo_available": rotativo_available,
            "rotativo_used": rotativo_used,
            "cheque_available": cheque_available,
            "cheque_used": cheque_used,
        }
        response = self.http_client.post(self.base_endpoint, data=data)
        return BankLimit.from_dict(response)

    def list_all(self) -> List[BankLimit]:
        response = self.http_client.get(self.base_endpoint)
        return [BankLimit.from_dict(limit) for limit in response]

    def update(
        self,
        limit_id: str,
        bank_name: str,
        rotativo_available: float = 0.0,
        rotativo_used: float = 0.0,
        cheque_available: float = 0.0,
        cheque_used: float = 0.0,
    ) -> BankLimit:
        data = {
            "bank_name": bank_name,
            "rotativo_available": rotativo_available,
            "rotativo_used": rotativo_used,
            "cheque_available": cheque_available,
            "cheque_used": cheque_used,
        }
        response = self.http_client.put(f"{self.base_endpoint}/{limit_id}", data=data)
        return BankLimit.from_dict(response)

    def delete(self, limit_id: str) -> bool:
        try:
            self.http_client.delete(f"{self.base_endpoint}/{limit_id}")
            return True
        except Exception:
            return False
