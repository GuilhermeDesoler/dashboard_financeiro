from domain.entities.platform_settings import PlatformSettings
from domain.repositories.platform_settings_repository import PlatformSettingsRepository


class PlatformSettingsUseCases:
    def __init__(self, repository: PlatformSettingsRepository):
        self.repository = repository

    def get_settings(self) -> PlatformSettings:
        """Get platform settings"""
        return self.repository.get_settings()

    def toggle_anticipation(self) -> PlatformSettings:
        """Toggle anticipation feature on/off"""
        return self.repository.toggle_anticipation()
