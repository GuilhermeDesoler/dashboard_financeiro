from domain.entities import AuthResponse, LoginRequest, RegisterRequest, User
from domain.repositories import AuthRepository


class AuthUseCases:
    def __init__(self, repository: AuthRepository):
        self.repository = repository

    def login(self, email: str, password: str) -> AuthResponse:
        request = LoginRequest(email=email, password=password)
        return self.repository.login(request)

    def register(
        self, email: str, password: str, name: str, company_name: str, cnpj: str
    ) -> dict:
        request = RegisterRequest(
            email=email,
            password=password,
            name=name,
            company_name=company_name,
            cnpj=cnpj,
        )
        return self.repository.register(request)

    def refresh_token(self, refresh_token: str) -> AuthResponse:
        return self.repository.refresh_token(refresh_token)

    def get_current_user(self, token: str) -> User:
        return self.repository.get_current_user(token)
