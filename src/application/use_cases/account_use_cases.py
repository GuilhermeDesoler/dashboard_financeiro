from typing import List, Optional
from datetime import datetime
from domain.entities.account import Account
from domain.repositories.account_repository import AccountRepository


class AccountUseCases:
    def __init__(self, repository: AccountRepository):
        self.repository = repository

    def create_account(
        self, value: float, date: datetime, description: str, account_type: str
    ) -> Account:
        """Create a new account entry"""
        return self.repository.create(value, date, description, account_type)

    def list_accounts(
        self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None
    ) -> List[Account]:
        """List all accounts, optionally filtered by date range"""
        return self.repository.list_all(start_date, end_date)

    def delete_account(self, account_id: str) -> bool:
        """Delete an account by ID"""
        return self.repository.delete(account_id)
