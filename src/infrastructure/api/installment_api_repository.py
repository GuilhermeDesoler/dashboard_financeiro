from typing import List, Optional, Dict, Any
from datetime import datetime
from domain.entities.installment import Installment
from domain.repositories.installment_repository import InstallmentRepository
from infrastructure.http import HTTPClient


class InstallmentAPIRepository(InstallmentRepository):
    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client
        self.base_endpoint = "/api/installments"

    def get_by_financial_entry(self, financial_entry_id: str) -> List[Installment]:
        response = self.http_client.get(
            self.base_endpoint, params={"financial_entry_id": financial_entry_id}
        )
        return [Installment.from_dict(item) for item in response]

    def get_by_id(self, installment_id: str) -> Optional[Installment]:
        try:
            response = self.http_client.get(f"{self.base_endpoint}/{installment_id}")
            return Installment.from_dict(response)
        except Exception:
            return None

    def pay_installment(
        self, installment_id: str, payment_date: Optional[datetime] = None
    ) -> Installment:
        data = {}
        if payment_date:
            data["payment_date"] = payment_date.isoformat()

        response = self.http_client.patch(
            f"{self.base_endpoint}/{installment_id}/pay", data=data
        )
        return Installment.from_dict(response)

    def unpay_installment(self, installment_id: str) -> Installment:
        response = self.http_client.patch(
            f"{self.base_endpoint}/{installment_id}/unpay", data={}
        )
        return Installment.from_dict(response)

    def get_daily_summary(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[Dict[str, Any]]:
        """
        Obtém resumo diário do crediário

        Returns:
            Lista de dicionários com:
            - date: Data do resumo
            - total_receivable: Total a receber (parcelas não pagas)
            - total_received: Total recebido (pagamentos de crediário)
            - difference: Diferença (recebido - a receber)
        """
        params = {}
        if start_date:
            params["start_date"] = start_date.strftime("%Y-%m-%d")
        if end_date:
            params["end_date"] = end_date.strftime("%Y-%m-%d")

        response = self.http_client.get(
            f"{self.base_endpoint}/daily-summary", params=params
        )
        return response
