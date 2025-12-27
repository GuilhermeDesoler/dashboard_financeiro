from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities import PaymentModality


class PaymentModalityRepository(ABC):
    @abstractmethod
    def create(self, modality: PaymentModality) -> PaymentModality:
        pass

    @abstractmethod
    def get_all(self) -> List[PaymentModality]:
        pass

    @abstractmethod
    def get_by_id(self, modality_id: str) -> Optional[PaymentModality]:
        pass

    @abstractmethod
    def update(self, modality_id: str, modality: PaymentModality) -> PaymentModality:
        pass

    @abstractmethod
    def delete(self, modality_id: str) -> bool:
        pass

    @abstractmethod
    def toggle(self, modality_id: str) -> PaymentModality:
        pass
