from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime
from domain.entities import FinancialEntry


class FinancialEntryRepository(ABC):
    @abstractmethod
    def create(
        self,
        entry: FinancialEntry,
        installments_count: Optional[int] = None,
        start_date: Optional[datetime] = None,
        is_credit_payment: bool = False,
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_all(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[FinancialEntry]:
        pass

    @abstractmethod
    def get_by_id(self, entry_id: str) -> Optional[FinancialEntry]:
        pass

    @abstractmethod
    def update(self, entry_id: str, entry: FinancialEntry) -> FinancialEntry:
        pass

    @abstractmethod
    def delete(self, entry_id: str) -> bool:
        pass
