"""
Admin use cases for company and user management
"""
from typing import List, Optional
from domain.repositories.company_repository import CompanyRepository
from domain.repositories.user_repository import UserRepository
from domain.entities.company import Company
from domain.entities.user import User


class AdminUseCases:
    """Admin business logic for managing companies and users"""

    def __init__(
        self,
        company_repository: CompanyRepository,
        user_repository: UserRepository
    ):
        self._company_repository = company_repository
        self._user_repository = user_repository

    # Company operations
    def get_all_companies(self, only_active: bool = True) -> List[Company]:
        """Get all companies"""
        return self._company_repository.get_all(only_active=only_active)

    def get_company_by_id(self, company_id: str) -> Optional[Company]:
        """Get company details by ID"""
        return self._company_repository.get_by_id(company_id)

    def create_company(
        self,
        name: str,
        cnpj: Optional[str] = None,
        phone: Optional[str] = None,
        plan: str = "basic"
    ) -> Company:
        """Create a new company"""
        company = Company(
            name=name,
            cnpj=cnpj,
            phone=phone,
            plan=plan
        )
        return self._company_repository.create(company)

    # User operations
    def get_all_users(
        self,
        company_id: Optional[str] = None,
        only_active: bool = True
    ) -> List[User]:
        """Get all users, optionally filtered by company"""
        return self._user_repository.get_all(
            company_id=company_id,
            only_active=only_active
        )

    def create_user(
        self,
        email: str,
        password: str,
        name: str,
        company_id: str,
        is_super_admin: bool = False
    ) -> User:
        """Create a new user"""
        return self._user_repository.create(
            email=email,
            password=password,
            name=name,
            company_id=company_id,
            is_super_admin=is_super_admin
        )

    def toggle_user_active(self, user_id: str, activate: bool) -> bool:
        """Activate or deactivate a user"""
        return self._user_repository.toggle_active(user_id, activate)
