from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class PlatformSettings:
    is_anticipation_enabled: bool = False
    id: str = "platform_settings"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "is_anticipation_enabled": self.is_anticipation_enabled,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @staticmethod
    def from_dict(data: dict) -> "PlatformSettings":
        return PlatformSettings(
            id=data.get("id", "platform_settings"),
            is_anticipation_enabled=data.get("is_anticipation_enabled", False),
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

    def toggle_anticipation(self) -> None:
        self.is_anticipation_enabled = not self.is_anticipation_enabled
        self.updated_at = datetime.now()
