from typing import List
from domain.entities import PaymentModality
from domain.repositories import PaymentModalityRepository


class PaymentModalityUseCases:
    def __init__(self, repository: PaymentModalityRepository):
        self.repository = repository

    def create_modality(self, name: str, color: str = "#9333EA", is_active: bool = True) -> PaymentModality:
        modality = PaymentModality(name=name, color=color, is_active=is_active)
        return self.repository.create(modality)

    def list_modalities(self) -> List[PaymentModality]:
        return self.repository.get_all()

    def list_active_modalities(self) -> List[PaymentModality]:
        all_modalities = self.repository.get_all()
        return [m for m in all_modalities if m.is_active]

    def update_modality(
        self, modality_id: str, name: str, color: str, is_active: bool
    ) -> PaymentModality:
        modality = PaymentModality(name=name, color=color, is_active=is_active)
        return self.repository.update(modality_id, modality)

    def delete_modality(self, modality_id: str) -> bool:
        return self.repository.delete(modality_id)

    def toggle_modality(self, modality_id: str) -> PaymentModality:
        return self.repository.toggle(modality_id)
