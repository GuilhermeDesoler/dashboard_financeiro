"""
Authentication repository interface
"""
from abc import ABC, abstractmethod
from domain.entities.auth import LoginCredentials, AuthToken, ImpersonateToken
from domain.entities.user import User


class AuthRepository(ABC):
    """Abstract repository for Authentication operations"""

    @abstractmethod
    def login(self, credentials: LoginCredentials) -> AuthToken:
        """
        Authenticate user and get tokens

        Args:
            credentials: Login credentials (email + password)

        Returns:
            AuthToken with JWT tokens and user data
        """
        pass

    @abstractmethod
    def refresh_token(self, refresh_token: str) -> AuthToken:
        """
        Refresh access token using refresh token

        Args:
            refresh_token: JWT refresh token

        Returns:
            New AuthToken with refreshed tokens
        """
        pass

    @abstractmethod
    def get_current_user(self, token: str) -> User:
        """
        Get current authenticated user

        Args:
            token: JWT access token

        Returns:
            User object
        """
        pass

    @abstractmethod
    def impersonate_company(self, company_id: str, token: str) -> ImpersonateToken:
        """
        Impersonate a company (super admin only)

        Args:
            company_id: Company UUID to impersonate
            token: Super admin JWT token

        Returns:
            ImpersonateToken with 1-hour token for the company
        """
        pass
