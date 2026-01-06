from typing import List, Optional, Dict, Any
from datetime import datetime
from domain.entities.installment import Installment
from domain.repositories.installment_repository import InstallmentRepository


class InstallmentUseCases:
    def __init__(self, repository: InstallmentRepository):
        self.repository = repository

    def list_installments(self, financial_entry_id: str) -> List[Installment]:
        """List all installments for a financial entry"""
        return self.repository.get_by_financial_entry(financial_entry_id)

    def get_installment(self, installment_id: str) -> Optional[Installment]:
        """Get a specific installment by ID"""
        return self.repository.get_by_id(installment_id)

    def pay_installment(
        self, installment_id: str, payment_date: Optional[datetime] = None
    ) -> Installment:
        """Mark an installment as paid"""
        return self.repository.pay_installment(installment_id, payment_date)

    def unpay_installment(self, installment_id: str) -> Installment:
        """Mark an installment as unpaid"""
        return self.repository.unpay_installment(installment_id)

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
        return self.repository.get_daily_summary(start_date, end_date)
