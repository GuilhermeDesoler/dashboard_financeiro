"""
Company repository interface
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.company import Company


class CompanyRepository(ABC):
    """Abstract repository for Company operations"""

    @abstractmethod
    def get_all(self, only_active: bool = True) -> List[Company]:
        """
        Get all companies

        Args:
            only_active: Only return active companies (default: True)

        Returns:
            List of Company objects
        """
        pass

    @abstractmethod
    def get_by_id(self, company_id: str) -> Optional[Company]:
        """
        Get company by ID with users list

        Args:
            company_id: Company UUID

        Returns:
            Company object with users_count populated, or None if not found
        """
        pass

    @abstractmethod
    def create(self, company: Company) -> Company:
        """
        Create a new company

        Args:
            company: Company object with data

        Returns:
            Created Company object with ID
        """
        pass
