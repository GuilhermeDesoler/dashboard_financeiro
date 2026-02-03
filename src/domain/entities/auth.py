"""
Auth entities - Authentication related data structures
"""
from dataclasses import dataclass
from typing import Optional
from domain.entities.user import User


@dataclass
class LoginCredentials:
    """
    Login credentials

    Attributes:
        email: User email
        password: User password
    """
    email: str
    password: str

    def to_dict(self):
        """Convert to dictionary for API requests"""
        return {
            "email": self.email,
            "password": self.password,
        }


@dataclass
class AuthToken:
    """
    Authentication token response

    Attributes:
        token: JWT access token
        refresh_token: JWT refresh token
        user: User data
    """
    token: str
    refresh_token: str
    user: User

    @staticmethod
    def from_dict(data: dict) -> 'AuthToken':
        """Create AuthToken from dictionary"""
        return AuthToken(
            token=data["token"],
            refresh_token=data["refresh_token"],
            user=User.from_dict(data["user"]),
        )


@dataclass
class ImpersonateToken:
    """
    Impersonate token response

    Attributes:
        token: Impersonate JWT token (24 hours expiry)
        company: Basic company info
        message: Success message
        expires_in_hours: Token expiry in hours
    """
    token: str
    company: dict
    message: str
    expires_in_hours: int = 24

    @staticmethod
    def from_dict(data: dict) -> 'ImpersonateToken':
        """Create ImpersonateToken from dictionary"""
        return ImpersonateToken(
            token=data["token"],
            company=data["company"],
            message=data["message"],
            expires_in_hours=data.get("expires_in_hours", 24),
        )
