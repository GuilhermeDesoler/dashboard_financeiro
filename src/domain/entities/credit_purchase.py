"""
Credit Purchase entity - Represents a credit purchase (installment plan)
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Literal


@dataclass
class CreditPurchase:
    """Credit purchase entity"""
    id: str
    pagante_nome: str
    descricao_compra: str
    valor_total: float
    valor_entrada: float
    numero_parcelas: int
    data_inicio_pagamento: datetime
    intervalo_dias: int
    taxa_juros_mensal: float
    registrado_por_user_id: str
    registrado_por_nome: str
    status: Literal["ativo", "cancelado", "concluido"]
    created_at: datetime
    updated_at: datetime
    pagante_documento: Optional[str] = None
    pagante_telefone: Optional[str] = None

    # Calculated fields
    total_pago: Optional[float] = None
    total_pendente: Optional[float] = None
    parcelas_pagas: Optional[int] = None
    parcelas_atrasadas: Optional[int] = None
    percentual_pago: Optional[float] = None


@dataclass
class CreditInstallment:
    """Credit installment entity"""
    id: str
    credit_purchase_id: str
    numero_parcela: int
    valor_parcela: float
    valor_juros: float
    valor_multa: float
    valor_total: float
    data_vencimento: datetime
    status: Literal["pendente", "pago", "atrasado", "cancelado"]
    observacao: str
    dias_atraso: int
    created_at: datetime
    updated_at: datetime
    data_pagamento: Optional[datetime] = None
    financial_entry_id: Optional[str] = None
    pago_por_user_id: Optional[str] = None
    pago_por_nome: Optional[str] = None

    # Enriched fields (from purchase)
    pagante_nome: Optional[str] = None
    descricao_compra: Optional[str] = None
    pagante_telefone: Optional[str] = None
