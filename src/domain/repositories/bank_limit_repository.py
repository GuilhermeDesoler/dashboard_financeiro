"""
Bank Limit Repository interface
"""
from abc import ABC, abstractmethod
from typing import List
from domain.entities.bank_limit import BankLimit


class BankLimitRepository(ABC):
    """Abstract repository for bank limits"""

    @abstractmethod
    def create(
        self,
        bank_name: str,
        rotativo_available: float = 0.0,
        rotativo_used: float = 0.0,
        cheque_available: float = 0.0,
        cheque_used: float = 0.0,
    ) -> BankLimit:
        """Create a new bank limit"""
        pass

    @abstractmethod
    def list_all(self) -> List[BankLimit]:
        """List all bank limits"""
        pass

    @abstractmethod
    def update(
        self,
        limit_id: str,
        bank_name: str,
        rotativo_available: float = 0.0,
        rotativo_used: float = 0.0,
        cheque_available: float = 0.0,
        cheque_used: float = 0.0,
    ) -> BankLimit:
        """Update a bank limit"""
        pass

    @abstractmethod
    def delete(self, limit_id: str) -> bool:
        """Delete a bank limit"""
        pass
