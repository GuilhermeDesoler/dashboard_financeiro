from typing import List, Optional
from datetime import datetime
from domain.entities import FinancialEntry
from domain.repositories import FinancialEntryRepository
from infrastructure.http import HTTPClient


class FinancialEntryAPIRepository(FinancialEntryRepository):
    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client
        self.base_endpoint = "/api/financial-entries"

    def create(self, entry: FinancialEntry) -> FinancialEntry:
        data = {
            "value": entry.value,
            "date": entry.date.isoformat(),
            "modality_id": entry.modality_id,
        }
        response = self.http_client.post(self.base_endpoint, data)
        return FinancialEntry.from_dict(response)

    def get_all(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[FinancialEntry]:
        params = {}
        if start_date:
            # Formato: YYYY-MM-DD (sem hora, apenas data)
            params["start_date"] = start_date.strftime("%Y-%m-%d")
        if end_date:
            # Formato: YYYY-MM-DD (sem hora, apenas data)
            params["end_date"] = end_date.strftime("%Y-%m-%d")

        response = self.http_client.get(self.base_endpoint, params=params)
        return [FinancialEntry.from_dict(item) for item in response]

    def get_by_id(self, entry_id: str) -> Optional[FinancialEntry]:
        try:
            response = self.http_client.get(f"{self.base_endpoint}/{entry_id}")
            return FinancialEntry.from_dict(response)
        except Exception:
            return None

    def update(self, entry_id: str, entry: FinancialEntry) -> FinancialEntry:
        data = {
            "value": entry.value,
            "date": entry.date.isoformat(),
            "modality_id": entry.modality_id,
        }
        response = self.http_client.put(f"{self.base_endpoint}/{entry_id}", data)
        return FinancialEntry.from_dict(response)

    def delete(self, entry_id: str) -> bool:
        return self.http_client.delete(f"{self.base_endpoint}/{entry_id}")
