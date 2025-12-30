from domain.entities import AuthResponse, LoginRequest, RegisterRequest, User
from domain.repositories import AuthRepository
from infrastructure.http import HTTPClient


class AuthAPIRepository(AuthRepository):
    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client
        self.base_endpoint = "/api/auth"

    def login(self, request: LoginRequest) -> AuthResponse:
        response = self.http_client.post(f"{self.base_endpoint}/login", request.to_dict())
        return AuthResponse.from_dict(response)

    def register(self, request: RegisterRequest) -> dict:
        response = self.http_client.post(f"{self.base_endpoint}/register", request.to_dict())
        return response

    def refresh_token(self, refresh_token: str) -> AuthResponse:
        response = self.http_client.post(f"{self.base_endpoint}/refresh", {"refresh_token": refresh_token})
        return AuthResponse.from_dict(response)

    def get_current_user(self, token: str) -> User:
        response = self.http_client.get(f"{self.base_endpoint}/me")
        return User.from_dict(response["user"])
