from typing import List, Optional
from datetime import datetime
from domain.entities.account import Account
from domain.repositories.account_repository import AccountRepository
from infrastructure.http import HTTPClient


class AccountAPIRepository(AccountRepository):
    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client
        self.base_endpoint = "/api/accounts"

    def create(self, value: float, date: datetime, description: str, account_type: str) -> Account:
        data = {
            "value": value,
            "date": date.isoformat(),
            "description": description,
            "type": account_type,
        }
        response = self.http_client.post(self.base_endpoint, data=data)
        return Account.from_dict(response)

    def list_all(
        self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None
    ) -> List[Account]:
        params = {}
        if start_date:
            params["start_date"] = start_date.isoformat()
        if end_date:
            params["end_date"] = end_date.isoformat()

        response = self.http_client.get(self.base_endpoint, params=params)
        return [Account.from_dict(account) for account in response]

    def update(self, account_id: str, paid: bool = None, value: float = None, date: datetime = None, description: str = None) -> Account:
        data = {}
        if paid is not None:
            data["paid"] = paid
        if value is not None:
            data["value"] = value
        if date is not None:
            data["date"] = date.isoformat()
        if description is not None:
            data["description"] = description

        response = self.http_client.patch(f"{self.base_endpoint}/{account_id}", data=data)
        return Account.from_dict(response)

    def delete(self, account_id: str) -> bool:
        try:
            self.http_client.delete(f"{self.base_endpoint}/{account_id}")
            return True
        except Exception:
            return False
