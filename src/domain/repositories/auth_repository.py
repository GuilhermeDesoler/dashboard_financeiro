from abc import ABC, abstractmethod
from domain.entities import AuthResponse, LoginRequest, RegisterRequest, User


class AuthRepository(ABC):
    @abstractmethod
    def login(self, request: LoginRequest) -> AuthResponse:
        pass

    @abstractmethod
    def register(self, request: RegisterRequest) -> dict:
        pass

    @abstractmethod
    def refresh_token(self, refresh_token: str) -> AuthResponse:
        pass

    @abstractmethod
    def get_current_user(self, token: str) -> User:
        pass
