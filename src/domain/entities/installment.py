from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Installment:
    financial_entry_id: str
    installment_number: int
    total_installments: int
    amount: float
    due_date: datetime
    is_paid: bool = False
    payment_date: Optional[datetime] = None
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "financial_entry_id": self.financial_entry_id,
            "installment_number": self.installment_number,
            "total_installments": self.total_installments,
            "amount": self.amount,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "is_paid": self.is_paid,
            "payment_date": self.payment_date.isoformat() if self.payment_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @staticmethod
    def from_dict(data: dict) -> "Installment":
        return Installment(
            id=data.get("id"),
            financial_entry_id=data["financial_entry_id"],
            installment_number=data["installment_number"],
            total_installments=data["total_installments"],
            amount=float(data["amount"]),
            due_date=Installment._parse_datetime(data["due_date"]),
            is_paid=data.get("is_paid", False),
            payment_date=Installment._parse_datetime(data.get("payment_date")),
            created_at=Installment._parse_datetime(data.get("created_at")),
            updated_at=Installment._parse_datetime(data.get("updated_at")),
        )

    @staticmethod
    def _parse_datetime(value) -> Optional[datetime]:
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        return datetime.fromisoformat(value.replace("Z", "+00:00"))

    def mark_as_paid(self, payment_date: Optional[datetime] = None) -> None:
        self.is_paid = True
        self.payment_date = payment_date or datetime.now()
        self.updated_at = datetime.now()

    def mark_as_unpaid(self) -> None:
        self.is_paid = False
        self.payment_date = None
        self.updated_at = datetime.now()
