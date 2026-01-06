from typing import List, Optional
from domain.entities import PaymentModality
from domain.repositories import PaymentModalityRepository
from infrastructure.http import HTTPClient


class PaymentModalityAPIRepository(PaymentModalityRepository):
    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client
        self.base_endpoint = "/api/payment-modalities"

    def create(self, modality: PaymentModality) -> PaymentModality:
        data = {
            "name": modality.name,
            "color": modality.color,
            "bank_name": modality.bank_name,
            "fee_percentage": modality.fee_percentage,
            "rental_fee": modality.rental_fee,
            "is_active": modality.is_active,
            "is_credit_plan": modality.is_credit_plan,
            "allows_anticipation": modality.allows_anticipation,
            "allows_credit_payment": modality.allows_credit_payment,
        }
        response = self.http_client.post(self.base_endpoint, data)
        return PaymentModality.from_dict(response)

    def get_all(self, only_active: bool = False) -> List[PaymentModality]:
        endpoint = f"{self.base_endpoint}?only_active={'true' if only_active else 'false'}"
        response = self.http_client.get(endpoint)
        return [PaymentModality.from_dict(item) for item in response]

    def get_by_id(self, modality_id: str) -> Optional[PaymentModality]:
        try:
            response = self.http_client.get(f"{self.base_endpoint}/{modality_id}")
            return PaymentModality.from_dict(response)
        except Exception:
            return None

    def update(self, modality_id: str, modality: PaymentModality) -> PaymentModality:
        data = {
            "name": modality.name,
            "color": modality.color,
            "bank_name": modality.bank_name,
            "fee_percentage": modality.fee_percentage,
            "rental_fee": modality.rental_fee,
            "is_active": modality.is_active,
            "is_credit_plan": modality.is_credit_plan,
            "allows_anticipation": modality.allows_anticipation,
            "allows_credit_payment": modality.allows_credit_payment,
        }
        response = self.http_client.put(f"{self.base_endpoint}/{modality_id}", data)
        return PaymentModality.from_dict(response)

    def delete(self, modality_id: str) -> bool:
        return self.http_client.delete(f"{self.base_endpoint}/{modality_id}")

    def toggle(self, modality_id: str) -> PaymentModality:
        response = self.http_client.patch(
            f"{self.base_endpoint}/{modality_id}/toggle",
            data={}
        )
        return PaymentModality.from_dict(response)
