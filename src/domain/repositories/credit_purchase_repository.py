"""
Credit Purchase Repository Interface
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime
from domain.entities.credit_purchase import CreditPurchase, CreditInstallment


class CreditPurchaseRepository(ABC):
    """Abstract repository for credit purchases"""

    @abstractmethod
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
        pass

    @abstractmethod
    def get_all_purchases(
        self,
        status: Optional[str] = None,
        pagante_nome: Optional[str] = None,
        page: int = 1,
        per_page: int = 20,
    ) -> Dict[str, Any]:
        """Get all credit purchases with pagination"""
        pass

    @abstractmethod
    def get_purchase_by_id(self, purchase_id: str) -> CreditPurchase:
        """Get a credit purchase by ID with all installments"""
        pass

    @abstractmethod
    def update_purchase(
        self,
        purchase_id: str,
        pagante_telefone: Optional[str] = None,
        pagante_documento: Optional[str] = None,
        descricao_compra: Optional[str] = None,
    ) -> CreditPurchase:
        """Update credit purchase information"""
        pass

    @abstractmethod
    def cancel_purchase(self, purchase_id: str) -> Dict[str, Any]:
        """Cancel a credit purchase and its pending installments"""
        pass

    @abstractmethod
    def delete_purchase(self, purchase_id: str) -> Dict[str, Any]:
        """Delete a credit purchase and all installments"""
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def unpay_installment(
        self,
        purchase_id: str,
        installment_id: str,
    ) -> CreditInstallment:
        """Remove payment from an installment"""
        pass

    @abstractmethod
    def get_installments_by_date(
        self,
        start_date: datetime,
        end_date: datetime,
        status: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get installments grouped by due date"""
        pass

    @abstractmethod
    def get_totals(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """Get totals summary"""
        pass

    @abstractmethod
    def get_overdue_installments(self) -> Dict[str, Any]:
        """Get all overdue installments"""
        pass

    @abstractmethod
    def get_due_soon_installments(self, days: int = 7) -> Dict[str, Any]:
        """Get installments due in the next N days"""
        pass
