from typing import Optional
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

    def update_markup_settings(
        self,
        markup_default: Optional[float] = None,
        markup_cost: Optional[float] = None,
        markup_percentage: Optional[float] = None
    ) -> PlatformSettings:
        data = {}
        if markup_default is not None:
            data["markup_default"] = markup_default
        if markup_cost is not None:
            data["markup_cost"] = markup_cost
        if markup_percentage is not None:
            data["markup_percentage"] = markup_percentage

        response = self.http_client.put(f"{self.base_endpoint}/markup", data)
        return PlatformSettings.from_dict(response)
