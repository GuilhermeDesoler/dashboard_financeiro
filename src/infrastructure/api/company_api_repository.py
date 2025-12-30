"""
Company API repository implementation
"""
from typing import List, Optional
from domain.repositories.company_repository import CompanyRepository
from domain.entities.company import Company
from infrastructure.http import HTTPClient


class CompanyAPIRepository(CompanyRepository):
    """API implementation of CompanyRepository"""

    def __init__(self, http_client: HTTPClient):
        self._http_client = http_client

    def get_all(self, only_active: bool = True) -> List[Company]:
        """Get all companies from API"""
        params = {
            "only_active": str(only_active).lower()
        }

        response = self._http_client.get("/api/admin/companies", params=params)
        return [Company.from_dict(company_data) for company_data in response]

    def get_by_id(self, company_id: str) -> Optional[Company]:
        """Get company by ID with users info"""
        try:
            response = self._http_client.get(f"/api/admin/companies/{company_id}")
            return Company.from_dict(response)
        except Exception:
            return None

    def create(self, company: Company) -> Company:
        """Create a new company via API"""
        response = self._http_client.post("/api/admin/companies", company.to_dict())
        return Company.from_dict(response["company"])
