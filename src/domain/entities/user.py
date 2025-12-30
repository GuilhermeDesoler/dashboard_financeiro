from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class User:
    email: str
    name: str
    company_id: str
    role_ids: List[str] = None
    is_active: bool = True
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if self.role_ids is None:
            self.role_ids = []

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "company_id": self.company_id,
            "role_ids": self.role_ids,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @staticmethod
    def from_dict(data: dict) -> "User":
        return User(
            id=data.get("id"),
            email=data["email"],
            name=data["name"],
            company_id=data["company_id"],
            role_ids=data.get("role_ids", []),
            is_active=data.get("is_active", True),
            created_at=User._parse_datetime(data.get("created_at")),
            updated_at=User._parse_datetime(data.get("updated_at")),
        )

    @staticmethod
    def _parse_datetime(value) -> Optional[datetime]:
        if value is None:
            return None
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
