from typing import List
from domain.entities import PaymentModality
from domain.repositories import PaymentModalityRepository


class PaymentModalityUseCases:
    def __init__(self, repository: PaymentModalityRepository):
        self.repository = repository

    def create_modality(
        self,
        name: str,
        color: str = "#9333EA",
        bank_name: str = "",
        fee_percentage: float = 0.0,
        rental_fee: float = 0.0,
        is_active: bool = True,
        is_credit_plan: bool = False,
        allows_anticipation: bool = False,
        allows_credit_payment: bool = False,
    ) -> PaymentModality:
        modality = PaymentModality(
            name=name,
            color=color,
            bank_name=bank_name,
            fee_percentage=fee_percentage,
            rental_fee=rental_fee,
            is_active=is_active,
            is_credit_plan=is_credit_plan,
            allows_anticipation=allows_anticipation,
            allows_credit_payment=allows_credit_payment,
        )
        return self.repository.create(modality)

    def list_modalities(self) -> List[PaymentModality]:
        return self.repository.get_all(only_active=False)

    def list_active_modalities(self) -> List[PaymentModality]:
        return self.repository.get_all(only_active=True)

    def update_modality(
        self,
        modality_id: str,
        name: str,
        color: str,
        bank_name: str = "",
        fee_percentage: float = 0.0,
        rental_fee: float = 0.0,
        is_active: bool = True,
        is_credit_plan: bool = False,
        allows_anticipation: bool = False,
        allows_credit_payment: bool = False,
    ) -> PaymentModality:
        modality = PaymentModality(
            id=modality_id,
            name=name,
            color=color,
            bank_name=bank_name,
            fee_percentage=fee_percentage,
            rental_fee=rental_fee,
            is_active=is_active,
            is_credit_plan=is_credit_plan,
            allows_anticipation=allows_anticipation,
            allows_credit_payment=allows_credit_payment,
        )
        return self.repository.update(modality_id, modality)

    def delete_modality(self, modality_id: str) -> bool:
        return self.repository.delete(modality_id)

    def toggle_modality(self, modality_id: str) -> PaymentModality:
        return self.repository.toggle(modality_id)
