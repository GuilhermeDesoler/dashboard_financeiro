"""
User API repository implementation
"""
from typing import List, Optional
from domain.repositories.user_repository import UserRepository
from domain.entities.user import User
from infrastructure.http import HTTPClient


class UserAPIRepository(UserRepository):
    """API implementation of UserRepository"""

    def __init__(self, http_client: HTTPClient):
        self._http_client = http_client

    def get_all(self, company_id: Optional[str] = None, only_active: bool = True) -> List[User]:
        """Get all users from API"""
        params = {
            "only_active": str(only_active).lower()
        }
        if company_id:
            params["company_id"] = company_id

        response = self._http_client.get("/api/admin/users", params=params)
        return [User.from_dict(user_data) for user_data in response]

    def create(self, email: str, password: str, name: str, company_id: str, is_super_admin: bool = False) -> User:
        """Create a new user via API"""
        data = {
            "email": email,
            "password": password,
            "name": name,
            "company_id": company_id,
            "is_super_admin": is_super_admin
        }

        response = self._http_client.post("/api/admin/users", data)
        return User.from_dict(response["user"])

    def toggle_active(self, user_id: str, activate: bool) -> bool:
        """Toggle user active status via API"""
        data = {
            "activate": activate
        }

        self._http_client.patch(f"/api/admin/users/{user_id}/toggle-active", data)
        return True
