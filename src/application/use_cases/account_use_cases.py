from typing import List, Optional
from datetime import datetime
from dateutil.relativedelta import relativedelta
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

    def create_recurring_account(
        self, value: float, date: datetime, description: str, account_type: str, recurrence: int = 1
    ) -> List[Account]:
        """Create recurring account entries for the specified number of months"""
        accounts = []
        for i in range(recurrence):
            entry_date = date + relativedelta(months=i)
            account = self.repository.create(value, entry_date, description, account_type)
            accounts.append(account)
        return accounts

    def list_accounts(
        self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None
    ) -> List[Account]:
        """List all accounts, optionally filtered by date range"""
        return self.repository.list_all(start_date, end_date)

    def update_account(self, account_id: str, paid: bool = None, value: float = None, date: datetime = None, description: str = None) -> Account:
        """Update an account (principalmente o status paid, mas também outros campos)"""
        return self.repository.update(account_id, paid=paid, value=value, date=date, description=description)

    def delete_account(self, account_id: str) -> bool:
        """Delete an account by ID"""
        return self.repository.delete(account_id)
