from typing import List, Optional
from domain.entities import PaymentModality
from domain.repositories import PaymentModalityRepository
from infrastructure.http import HTTPClient


class PaymentModalityAPIRepository(PaymentModalityRepository):
    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client
        self.base_endpoint = "/api/payment-modalities"

    def create(self, modality: PaymentModality) -> PaymentModality:
        data = {"name": modality.name, "color": modality.color, "is_active": modality.is_active}
        response = self.http_client.post(self.base_endpoint, data)
        return PaymentModality.from_dict(response)

    def get_all(self) -> List[PaymentModality]:
        response = self.http_client.get(self.base_endpoint)
        return [PaymentModality.from_dict(item) for item in response]

    def get_by_id(self, modality_id: str) -> Optional[PaymentModality]:
        try:
            response = self.http_client.get(f"{self.base_endpoint}/{modality_id}")
            return PaymentModality.from_dict(response)
        except Exception:
            return None

    def update(self, modality_id: str, modality: PaymentModality) -> PaymentModality:
        data = {"name": modality.name, "color": modality.color, "is_active": modality.is_active}
        response = self.http_client.put(f"{self.base_endpoint}/{modality_id}", data)
        return PaymentModality.from_dict(response)

    def delete(self, modality_id: str) -> bool:
        return self.http_client.delete(f"{self.base_endpoint}/{modality_id}")

    def toggle(self, modality_id: str) -> PaymentModality:
        response = self.http_client.patch(f"{self.base_endpoint}/{modality_id}/toggle")
        return PaymentModality.from_dict(response)
