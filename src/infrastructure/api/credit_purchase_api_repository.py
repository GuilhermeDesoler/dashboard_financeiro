"""
Credit Purchase API Repository Implementation
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from domain.entities.credit_purchase import CreditPurchase, CreditInstallment
from domain.repositories.credit_purchase_repository import CreditPurchaseRepository
from infrastructure.http.http_client import HTTPClient


def _parse_datetime(date_string: str) -> datetime:
    """Parse datetime from various formats (ISO 8601 or GMT format)"""
    if not date_string:
        return datetime.now()

    # Remove 'Z' and replace with timezone if present
    date_string = date_string.replace("Z", "+00:00")

    # Try ISO format first
    try:
        return datetime.fromisoformat(date_string)
    except (ValueError, AttributeError):
        pass

    # Try GMT format (e.g., 'Fri, 30 Jan 2026 00:00:00 GMT')
    try:
        return datetime.strptime(date_string, "%a, %d %b %Y %H:%M:%S %Z")
    except (ValueError, AttributeError):
        pass

    # Try without timezone
    try:
        return datetime.strptime(date_string, "%a, %d %b %Y %H:%M:%S")
    except (ValueError, AttributeError):
        pass

    # Fallback to now
    return datetime.now()


class CreditPurchaseAPIRepository(CreditPurchaseRepository):
    """API implementation of Credit Purchase Repository"""

    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client

    def create_purchase(
        self,
        pagante_nome: str,
        descricao_compra: str,
        valor_total: float,
        numero_parcelas: int,
        data_inicio_pagamento: datetime,
        valor_entrada: float = 0.0,
        intervalo_dias: int = 30,
        taxa_juros_mensal: float = 0.0,
        pagante_documento: Optional[str] = None,
        pagante_telefone: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a new credit purchase with installments"""
        payload = {
            "pagante_nome": pagante_nome,
            "descricao_compra": descricao_compra,
            "valor_total": valor_total,
            "numero_parcelas": numero_parcelas,
            "data_inicio_pagamento": data_inicio_pagamento.isoformat(),
            "valor_entrada": valor_entrada,
            "intervalo_dias": intervalo_dias,
            "taxa_juros_mensal": taxa_juros_mensal,
        }

        if pagante_documento:
            payload["pagante_documento"] = pagante_documento
        if pagante_telefone:
            payload["pagante_telefone"] = pagante_telefone

        data = self.http_client.post("/api/credit-purchases", data=payload)

        # Parse response
        purchase_data = data["credit_purchase"]
        installments_data = data["installments"]

        purchase = self._parse_purchase(purchase_data)
        installments = [self._parse_installment(inst) for inst in installments_data]

        return {
            "credit_purchase": purchase,
            "installments": installments
        }

    def get_all_purchases(
        self,
        status: Optional[str] = None,
        pagante_nome: Optional[str] = None,
        page: int = 1,
        per_page: int = 20,
    ) -> Dict[str, Any]:
        """Get all credit purchases with pagination"""
        params = {
            "page": page,
            "per_page": per_page,
        }

        if status:
            params["status"] = status
        if pagante_nome:
            params["pagante_nome"] = pagante_nome

        data = self.http_client.get("/api/credit-purchases", params=params)

        return {
            "items": [self._parse_purchase(item) for item in data["items"]],
            "total": data["total"],
            "page": data["page"],
            "per_page": data["per_page"],
        }

    def get_purchase_by_id(self, purchase_id: str) -> CreditPurchase:
        """Get a credit purchase by ID with all installments"""
        data = self.http_client.get(f"/api/credit-purchases/{purchase_id}")

        purchase = self._parse_purchase(data)

        # Add installments if present
        if "installments" in data:
            purchase.installments = [
                self._parse_installment(inst) for inst in data["installments"]
            ]

        return purchase

    def update_purchase(
        self,
        purchase_id: str,
        pagante_telefone: Optional[str] = None,
        pagante_documento: Optional[str] = None,
        descricao_compra: Optional[str] = None,
    ) -> CreditPurchase:
        """Update credit purchase information"""
        payload = {}

        if pagante_telefone is not None:
            payload["pagante_telefone"] = pagante_telefone
        if pagante_documento is not None:
            payload["pagante_documento"] = pagante_documento
        if descricao_compra is not None:
            payload["descricao_compra"] = descricao_compra

        data = self.http_client.put(
            f"/api/credit-purchases/{purchase_id}",
            data=payload
        )
        return self._parse_purchase(data)

    def cancel_purchase(self, purchase_id: str) -> Dict[str, Any]:
        """Cancel a credit purchase and its pending installments"""
        data = self.http_client.patch(
            f"/api/credit-purchases/{purchase_id}/cancel"
        )

        return {
            "credit_purchase": self._parse_purchase(data["credit_purchase"]),
            "canceled_installments": data["canceled_installments"],
        }

    def delete_purchase(self, purchase_id: str) -> Dict[str, Any]:
        """Delete a credit purchase and all installments"""
        return self.http_client.delete(f"/api/credit-purchases/{purchase_id}")

    def pay_installment(
        self,
        purchase_id: str,
        installment_id: str,
        data_pagamento: datetime,
        modality_id: str,
        valor_juros: float = 0.0,
        valor_multa: float = 0.0,
        observacao: str = "",
    ) -> Dict[str, Any]:
        """Register payment for an installment"""
        payload = {
            "data_pagamento": data_pagamento.isoformat(),
            "modality_id": modality_id,
            "valor_juros": valor_juros,
            "valor_multa": valor_multa,
            "observacao": observacao,
        }

        data = self.http_client.post(
            f"/api/credit-purchases/{purchase_id}/installments/{installment_id}/pay",
            data=payload
        )

        return {
            "installment": self._parse_installment(data["installment"]),
            "financial_entry": data.get("financial_entry"),
        }

    def unpay_installment(
        self,
        purchase_id: str,
        installment_id: str,
    ) -> CreditInstallment:
        """Remove payment from an installment"""
        data = self.http_client.post(
            f"/api/credit-purchases/{purchase_id}/installments/{installment_id}/unpay",
            data={}
        )
        return self._parse_installment(data["installment"])

    def get_installments_by_date(
        self,
        start_date: datetime,
        end_date: datetime,
        status: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get installments grouped by due date"""
        params = {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        }

        if status:
            params["status"] = status

        data = self.http_client.get(
            "/api/credit-purchases/dashboard/installments-by-date",
            params=params
        )

        # Parse installments by date
        installments_by_date = []
        for date_group in data.get("installments_by_date", []):
            installments_by_date.append({
                "data_vencimento": date_group["data_vencimento"],
                "total_dia": date_group["total_dia"],
                "quantidade_parcelas": date_group["quantidade_parcelas"],
                "installments": [
                    self._parse_installment(inst)
                    for inst in date_group["installments"]
                ],
            })

        return {
            "period": data["period"],
            "summary": data["summary"],
            "installments_by_date": installments_by_date,
        }

    def get_totals(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """Get totals summary"""
        params = {}

        if start_date:
            params["start_date"] = start_date.isoformat()
        if end_date:
            params["end_date"] = end_date.isoformat()

        return self.http_client.get(
            "/api/credit-purchases/dashboard/totals",
            params=params
        )

    def get_overdue_installments(self) -> Dict[str, Any]:
        """Get all overdue installments"""
        data = self.http_client.get("/api/credit-purchases/dashboard/overdue")

        return {
            "total_atrasado": data["total_atrasado"],
            "quantidade_parcelas": data["quantidade_parcelas"],
            "installments": [
                self._parse_installment(inst) for inst in data["installments"]
            ],
        }

    def get_due_soon_installments(self, days: int = 7) -> Dict[str, Any]:
        """Get installments due in the next N days"""
        params = {"days": days}

        data = self.http_client.get(
            "/api/credit-purchases/dashboard/due-soon",
            params=params
        )

        return {
            "periodo_dias": data["periodo_dias"],
            "total_valor": data["total_valor"],
            "quantidade_parcelas": data["quantidade_parcelas"],
            "installments": [
                self._parse_installment(inst) for inst in data["installments"]
            ],
        }

    def _parse_purchase(self, data: Dict[str, Any]) -> CreditPurchase:
        """Parse API response to CreditPurchase entity"""
        return CreditPurchase(
            id=data.get("id", ""),
            pagante_nome=data.get("pagante_nome", ""),
            descricao_compra=data.get("descricao_compra", ""),
            valor_total=data.get("valor_total", 0.0),
            valor_entrada=data.get("valor_entrada", 0.0),
            numero_parcelas=data.get("numero_parcelas", 0),
            data_inicio_pagamento=_parse_datetime(
                data.get("data_inicio_pagamento", datetime.now().isoformat())
            ),
            intervalo_dias=data.get("intervalo_dias", 30),
            taxa_juros_mensal=data.get("taxa_juros_mensal", 0.0),
            registrado_por_user_id=data.get("registrado_por_user_id", ""),
            registrado_por_nome=data.get("registrado_por_nome", ""),
            status=data.get("status", "ativo"),
            created_at=_parse_datetime(
                data.get("created_at", datetime.now().isoformat())
            ),
            updated_at=_parse_datetime(
                data.get("updated_at", datetime.now().isoformat())
            ),
            pagante_documento=data.get("pagante_documento"),
            pagante_telefone=data.get("pagante_telefone"),
            total_pago=data.get("total_pago"),
            total_pendente=data.get("total_pendente"),
            parcelas_pagas=data.get("parcelas_pagas"),
            parcelas_atrasadas=data.get("parcelas_atrasadas"),
            percentual_pago=data.get("percentual_pago"),
        )

    def _parse_installment(self, data: Dict[str, Any]) -> CreditInstallment:
        """Parse API response to CreditInstallment entity"""
        return CreditInstallment(
            id=data.get("id", ""),
            credit_purchase_id=data.get("credit_purchase_id", ""),
            numero_parcela=data.get("numero_parcela", 0),
            valor_parcela=data.get("valor_parcela", 0.0),
            valor_juros=data.get("valor_juros", 0.0),
            valor_multa=data.get("valor_multa", 0.0),
            valor_total=data.get("valor_total", 0.0),
            data_vencimento=_parse_datetime(
                data.get("data_vencimento", datetime.now().isoformat())
            ),
            status=data.get("status", "pendente"),
            observacao=data.get("observacao", ""),
            dias_atraso=data.get("dias_atraso", 0),
            created_at=_parse_datetime(
                data.get("created_at", datetime.now().isoformat())
            ),
            updated_at=_parse_datetime(
                data.get("updated_at", datetime.now().isoformat())
            ),
            data_pagamento=_parse_datetime(data["data_pagamento"]) if data.get("data_pagamento") else None,
            financial_entry_id=data.get("financial_entry_id"),
            pago_por_user_id=data.get("pago_por_user_id"),
            pago_por_nome=data.get("pago_por_nome"),
            pagante_nome=data.get("pagante_nome"),
            descricao_compra=data.get("descricao_compra"),
            pagante_telefone=data.get("pagante_telefone"),
        )
