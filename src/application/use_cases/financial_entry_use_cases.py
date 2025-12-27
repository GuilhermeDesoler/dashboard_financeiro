from typing import List, Optional
from datetime import datetime
from domain.entities import FinancialEntry
from domain.repositories import FinancialEntryRepository


class FinancialEntryUseCases:
    def __init__(self, repository: FinancialEntryRepository):
        self.repository = repository

    def create_entry(
        self, value: float, date: datetime, modality_id: str, modality_name: str
    ) -> FinancialEntry:
        entry = FinancialEntry(
            value=value,
            date=date,
            modality_id=modality_id,
            modality_name=modality_name,
        )
        return self.repository.create(entry)

    def list_entries(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[FinancialEntry]:
        return self.repository.get_all(start_date, end_date)

    def update_entry(
        self,
        entry_id: str,
        value: float,
        date: datetime,
        modality_id: str,
        modality_name: str,
    ) -> FinancialEntry:
        entry = FinancialEntry(
            value=value,
            date=date,
            modality_id=modality_id,
            modality_name=modality_name,
        )
        return self.repository.update(entry_id, entry)

    def delete_entry(self, entry_id: str) -> bool:
        return self.repository.delete(entry_id)

    def get_total_by_period(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> float:
        entries = self.list_entries(start_date, end_date)
        return sum(entry.value for entry in entries)

    def get_entries_grouped_by_modality(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> dict:
        entries = self.list_entries(start_date, end_date)
        grouped = {}
        for entry in entries:
            if entry.modality_name not in grouped:
                grouped[entry.modality_name] = []
            grouped[entry.modality_name].append(entry)
        return grouped
