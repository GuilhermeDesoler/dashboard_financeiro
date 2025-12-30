"""
Authentication API repository implementation
"""
from domain.repositories.auth_repository import AuthRepository
from domain.entities.auth import LoginCredentials, AuthToken, ImpersonateToken
from domain.entities.user import User
from infrastructure.http import HTTPClient


class AuthAPIRepository(AuthRepository):
    """API implementation of AuthRepository"""

    def __init__(self, http_client: HTTPClient):
        self._http_client = http_client

    def login(self, credentials: LoginCredentials) -> AuthToken:
        """Login via API"""
        response = self._http_client.post("/api/auth/login", credentials.to_dict())
        return AuthToken.from_dict(response)

    def refresh_token(self, refresh_token: str) -> AuthToken:
        """Refresh token via API"""
        data = {
            "refresh_token": refresh_token
        }
        response = self._http_client.post("/api/auth/refresh", data)
        return AuthToken.from_dict(response)

    def get_current_user(self, token: str) -> User:
        """Get current user via API"""
        # Temporarily set token for this request
        original_token = self._http_client._auth_token
        self._http_client.set_auth_token(token)

        try:
            response = self._http_client.get("/api/auth/me")
            return User(
                id=response["user_id"],
                email=response["email"],
                name=response["name"],
                company_id=response["company_id"],
                role_ids=response.get("roles", []),
                features=response.get("features", []),
                is_super_admin=response.get("is_super_admin", False),
                is_active=True,
            )
        finally:
            # Restore original token
            self._http_client.set_auth_token(original_token)

    def impersonate_company(self, company_id: str, token: str) -> ImpersonateToken:
        """Impersonate company via API"""
        # Temporarily set token for this request
        original_token = self._http_client._auth_token
        self._http_client.set_auth_token(token)

        try:
            response = self._http_client.post(f"/api/admin/impersonate/{company_id}", {})
            return ImpersonateToken.from_dict(response)
        finally:
            # Restore original token
            self._http_client.set_auth_token(original_token)
