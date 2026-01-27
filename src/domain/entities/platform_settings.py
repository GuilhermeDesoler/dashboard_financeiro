from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class PlatformSettings:
    markup_default: float = 0.0  # M - Markup padrão
    markup_cost: float = 0.0  # C - Constante de custo adicional
    markup_percentage: float = 0.0  # Percentual de aumento (ex: 0.05 = 5%)
    id: str = "platform_settings"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "markup_default": self.markup_default,
            "markup_cost": self.markup_cost,
            "markup_percentage": self.markup_percentage,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @staticmethod
    def from_dict(data: dict) -> "PlatformSettings":
        return PlatformSettings(
            id=data.get("id", "platform_settings"),
            markup_default=data.get("markup_default", 0.0),
            markup_cost=data.get("markup_cost", 0.0),
            markup_percentage=data.get("markup_percentage", 0.0),
            created_at=PlatformSettings._parse_datetime(data.get("created_at")),
            updated_at=PlatformSettings._parse_datetime(data.get("updated_at")),
        )

    @staticmethod
    def _parse_datetime(value) -> Optional[datetime]:
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        return datetime.fromisoformat(value.replace("Z", "+00:00"))

    def get_multiplier(self) -> float:
        """Retorna o multiplicador A (1 + percentual)"""
        return 1 + self.markup_percentage
