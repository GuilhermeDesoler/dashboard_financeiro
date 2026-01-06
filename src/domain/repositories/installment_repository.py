from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from domain.entities.installment import Installment


class InstallmentRepository(ABC):
    @abstractmethod
    def get_by_financial_entry(self, financial_entry_id: str) -> List[Installment]:
        pass

    @abstractmethod
    def get_by_id(self, installment_id: str) -> Optional[Installment]:
        pass

    @abstractmethod
    def pay_installment(
        self, installment_id: str, payment_date: Optional[datetime] = None
    ) -> Installment:
        pass

    @abstractmethod
    def unpay_installment(self, installment_id: str) -> Installment:
        pass
