"""
Credit Purchase Use Cases
"""
from typing import Optional, Dict, Any
from datetime import datetime
from domain.repositories.credit_purchase_repository import CreditPurchaseRepository
from domain.entities.credit_purchase import CreditPurchase, CreditInstallment


class CreditPurchaseUseCases:
    """Use cases for credit purchase management"""

    def __init__(self, credit_purchase_repository: CreditPurchaseRepository):
        self.repository = credit_purchase_repository

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
        """
        Create a new credit purchase with installments

        Returns dict with credit_purchase and installments
        """
        return self.repository.create_purchase(
            pagante_nome=pagante_nome,
            descricao_compra=descricao_compra,
            valor_total=valor_total,
            numero_parcelas=numero_parcelas,
            data_inicio_pagamento=data_inicio_pagamento,
            valor_entrada=valor_entrada,
            intervalo_dias=intervalo_dias,
            taxa_juros_mensal=taxa_juros_mensal,
            pagante_documento=pagante_documento,
            pagante_telefone=pagante_telefone,
        )

    def get_all_purchases(
        self,
        status: Optional[str] = None,
        pagante_nome: Optional[str] = None,
        page: int = 1,
        per_page: int = 20,
    ) -> Dict[str, Any]:
        """Get all credit purchases with filters and pagination"""
        return self.repository.get_all_purchases(
            status=status,
            pagante_nome=pagante_nome,
            page=page,
            per_page=per_page,
        )

    def get_purchase_details(self, purchase_id: str) -> CreditPurchase:
        """Get complete purchase details including all installments"""
        return self.repository.get_purchase_by_id(purchase_id)

    def update_purchase(
        self,
        purchase_id: str,
        pagante_telefone: Optional[str] = None,
        pagante_documento: Optional[str] = None,
        descricao_compra: Optional[str] = None,
    ) -> CreditPurchase:
        """Update purchase information"""
        return self.repository.update_purchase(
            purchase_id=purchase_id,
            pagante_telefone=pagante_telefone,
            pagante_documento=pagante_documento,
            descricao_compra=descricao_compra,
        )

    def cancel_purchase(self, purchase_id: str) -> Dict[str, Any]:
        """Cancel a purchase and all pending installments"""
        return self.repository.cancel_purchase(purchase_id)

    def delete_purchase(self, purchase_id: str) -> Dict[str, Any]:
        """Delete a purchase (use with caution)"""
        return self.repository.delete_purchase(purchase_id)

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
        """
        Register payment for an installment

        Returns dict with installment and financial_entry
        """
        return self.repository.pay_installment(
            purchase_id=purchase_id,
            installment_id=installment_id,
            data_pagamento=data_pagamento,
            modality_id=modality_id,
            valor_juros=valor_juros,
            valor_multa=valor_multa,
            observacao=observacao,
        )

    def unpay_installment(
        self,
        purchase_id: str,
        installment_id: str,
    ) -> CreditInstallment:
        """Remove payment from an installment"""
        return self.repository.unpay_installment(
            purchase_id=purchase_id,
            installment_id=installment_id,
        )

    def get_dashboard_by_date(
        self,
        start_date: datetime,
        end_date: datetime,
        status: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get installments grouped by due date for dashboard

        Returns period, summary, and installments_by_date
        """
        return self.repository.get_installments_by_date(
            start_date=start_date,
            end_date=end_date,
            status=status,
        )

    def get_totals(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """Get general totals"""
        return self.repository.get_totals(
            start_date=start_date,
            end_date=end_date,
        )

    def get_overdue_installments(self) -> Dict[str, Any]:
        """Get all overdue installments"""
        return self.repository.get_overdue_installments()

    def get_due_soon(self, days: int = 7) -> Dict[str, Any]:
        """Get installments due soon"""
        return self.repository.get_due_soon_installments(days=days)
