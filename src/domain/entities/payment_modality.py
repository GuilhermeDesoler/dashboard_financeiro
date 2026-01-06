from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class PaymentModality:
    name: str
    color: str = "#9333EA"
    bank_name: str = ""
    fee_percentage: float = 0.0
    rental_fee: float = 0.0
    is_active: bool = True
    is_credit_plan: bool = False
    allows_anticipation: bool = False
    allows_credit_payment: bool = False
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color,
            "bank_name": self.bank_name,
            "fee_percentage": self.fee_percentage,
            "rental_fee": self.rental_fee,
            "is_active": self.is_active,
            "is_credit_plan": self.is_credit_plan,
            "allows_anticipation": self.allows_anticipation,
            "allows_credit_payment": self.allows_credit_payment,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @staticmethod
    def from_dict(data: dict) -> "PaymentModality":
        return PaymentModality(
            id=data.get("id"),
            name=data["name"],
            color=data.get("color", "#9333EA"),
            bank_name=data.get("bank_name", ""),
            fee_percentage=float(data.get("fee_percentage", 0.0)),
            rental_fee=float(data.get("rental_fee", 0.0)),
            is_active=data.get("is_active", True),
            is_credit_plan=data.get("is_credit_plan", False),
            allows_anticipation=data.get("allows_anticipation", False),
            allows_credit_payment=data.get("allows_credit_payment", False),
            created_at=PaymentModality._parse_datetime(data.get("created_at")),
            updated_at=PaymentModality._parse_datetime(data.get("updated_at")),
        )

    @staticmethod
    def _parse_datetime(value) -> Optional[datetime]:
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        return datetime.fromisoformat(value.replace("Z", "+00:00"))

    def activate(self) -> None:
        self.is_active = True
        self.updated_at = datetime.now()

    def deactivate(self) -> None:
        self.is_active = False
        self.updated_at = datetime.now()
