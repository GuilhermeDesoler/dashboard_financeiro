from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from domain.entities.account import Account


class AccountRepository(ABC):
    @abstractmethod
    def create(self, value: float, date: datetime, description: str, account_type: str) -> Account:
        pass

    @abstractmethod
    def list_all(
        self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None
    ) -> List[Account]:
        pass

    @abstractmethod
    def delete(self, account_id: str) -> bool:
        pass
