from abc import ABC, abstractmethod
from domain.entities.platform_settings import PlatformSettings


class PlatformSettingsRepository(ABC):
    @abstractmethod
    def get_settings(self) -> PlatformSettings:
        pass

    @abstractmethod
    def toggle_anticipation(self) -> PlatformSettings:
        pass
