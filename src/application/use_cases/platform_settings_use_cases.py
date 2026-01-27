from typing import Optional
from domain.entities.platform_settings import PlatformSettings
from domain.repositories.platform_settings_repository import PlatformSettingsRepository


class PlatformSettingsUseCases:
    def __init__(self, repository: PlatformSettingsRepository):
        self.repository = repository

    def get_settings(self) -> PlatformSettings:
        """Get platform settings"""
        return self.repository.get_settings()

    def update_markup_settings(
        self,
        markup_default: Optional[float] = None,
        markup_cost: Optional[float] = None,
        markup_percentage: Optional[float] = None
    ) -> PlatformSettings:
        """Update markup settings (admin only)"""
        return self.repository.update_markup_settings(
            markup_default=markup_default,
            markup_cost=markup_cost,
            markup_percentage=markup_percentage
        )
