"""
Bank Limit Use Cases
"""
from typing import List
from domain.entities.bank_limit import BankLimit
from domain.repositories.bank_limit_repository import BankLimitRepository


class BankLimitUseCases:
    def __init__(self, repository: BankLimitRepository):
        self.repository = repository

    def create_bank_limit(
        self,
        bank_name: str,
        rotativo_available: float = 0.0,
        rotativo_used: float = 0.0,
        cheque_available: float = 0.0,
        cheque_used: float = 0.0,
    ) -> BankLimit:
        """Create a new bank limit"""
        return self.repository.create(
            bank_name, rotativo_available, rotativo_used, cheque_available, cheque_used
        )

    def list_bank_limits(self) -> List[BankLimit]:
        """List all bank limits"""
        return self.repository.list_all()

    def update_bank_limit(
        self,
        limit_id: str,
        bank_name: str,
        rotativo_available: float = 0.0,
        rotativo_used: float = 0.0,
        cheque_available: float = 0.0,
        cheque_used: float = 0.0,
    ) -> BankLimit:
        """Update a bank limit"""
        return self.repository.update(
            limit_id, bank_name, rotativo_available, rotativo_used, cheque_available, cheque_used
        )

    def delete_bank_limit(self, limit_id: str) -> bool:
        """Delete a bank limit"""
        return self.repository.delete(limit_id)
