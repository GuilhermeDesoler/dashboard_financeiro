from domain.entities.platform_settings import PlatformSettings
from domain.repositories.platform_settings_repository import PlatformSettingsRepository
from infrastructure.http import HTTPClient


class PlatformSettingsAPIRepository(PlatformSettingsRepository):
    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client
        self.base_endpoint = "/api/platform-settings"

    def get_settings(self) -> PlatformSettings:
        response = self.http_client.get(self.base_endpoint)
        return PlatformSettings.from_dict(response)

    def toggle_anticipation(self) -> PlatformSettings:
        response = self.http_client.patch(f"{self.base_endpoint}/toggle-anticipation")
        return PlatformSettings.from_dict(response)
