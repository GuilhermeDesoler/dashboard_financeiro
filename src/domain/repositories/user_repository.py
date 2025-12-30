"""
User repository interface
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.user import User


class UserRepository(ABC):
    """Abstract repository for User operations"""

    @abstractmethod
    def get_all(self, company_id: Optional[str] = None, only_active: bool = True) -> List[User]:
        """
        Get all users, optionally filtered by company and active status

        Args:
            company_id: Filter by company UUID (optional)
            only_active: Only return active users (default: True)

        Returns:
            List of User objects
        """
        pass

    @abstractmethod
    def create(self, email: str, password: str, name: str, company_id: str, is_super_admin: bool = False) -> User:
        """
        Create a new user

        Args:
            email: User email
            password: User password (will be hashed by backend)
            name: User full name
            company_id: Company UUID
            is_super_admin: Whether user is super admin (default: False)

        Returns:
            Created User object
        """
        pass

    @abstractmethod
    def toggle_active(self, user_id: str, activate: bool) -> bool:
        """
        Activate or deactivate a user

        Args:
            user_id: User UUID
            activate: True to activate, False to deactivate

        Returns:
            True if successful
        """
        pass
