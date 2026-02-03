"""
Authentication use cases
"""
from domain.repositories.auth_repository import AuthRepository
from domain.entities.auth import LoginCredentials, AuthToken, ImpersonateToken
from domain.entities.user import User


class AuthUseCases:
    """Authentication business logic"""

    def __init__(self, auth_repository: AuthRepository):
        self._auth_repository = auth_repository

    def login(self, email: str, password: str) -> AuthToken:
        """
        Login user and get authentication tokens

        Args:
            email: User email
            password: User password

        Returns:
            AuthToken with JWT tokens and user data
        """
        credentials = LoginCredentials(email=email, password=password)
        return self._auth_repository.login(credentials)

    def refresh_token(self, refresh_token: str) -> AuthToken:
        """
        Refresh access token

        Args:
            refresh_token: Current refresh token

        Returns:
            New AuthToken with refreshed tokens
        """
        return self._auth_repository.refresh_token(refresh_token)

    def get_current_user(self, token: str) -> User:
        """
        Get current authenticated user

        Args:
            token: JWT access token

        Returns:
            User object
        """
        return self._auth_repository.get_current_user(token)

    def impersonate_company(self, company_id: str, token: str) -> ImpersonateToken:
        """
        Impersonate a company (super admin only)

        Args:
            company_id: Company UUID to impersonate
            token: Super admin JWT token

        Returns:
            ImpersonateToken with 24-hour token for the company
        """
        return self._auth_repository.impersonate_company(company_id, token)

    def change_password(self, current_password: str, new_password: str) -> bool:
        """
        Change user password

        Args:
            current_password: Current password
            new_password: New password

        Returns:
            True if password was changed successfully

        Raises:
            Exception if current password is incorrect or new password is invalid
        """
        return self._auth_repository.change_password(current_password, new_password)
