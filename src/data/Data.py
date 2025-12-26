from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, TypedDict


class TransactionType(str, Enum):
    DINHEIRO = "dinheiro"
    PIX_SICREDI = "pix_sicredi"
    PIX_SICOOB = "pix_sicoob"
    DEBITO_SICREDI = "debito_sicredi"
    DEBITO_SICOOB = "debito_sicoob"
    CREDITO_AV_SICREDI = "credito_av_sicredi"
    CREDITO_AV_SICOOB = "credito_av_sicoob"
    PARCELADO_2_4_SICREDI = "parcelado_2_4_sicredi"
    PARCELADO_2_4_SICOOB = "parcelado_2_4_sicoob"
    PARCELADO_5_6_SICREDI = "parcelado_5_6_sicredi"
    PARCELADO_5_6_SICOOB = "parcelado_5_6_sicoob"
    CREDIARIO = "crediario"
    RECEBIMENTO_CREDITARIO = "recebimento_creditario"
    BONUS_CRED = "bonus_cred"


@dataclass
class Transaction(TypedDict):
    valor: float
    type: TransactionType


DATA: Dict[str, List[Transaction]] = defaultdict(list)

# Dados de exemplo
DATA["25/12/2025"] = [
    Transaction(valor=50.00, type=TransactionType.PIX_SICREDI),
    Transaction(valor=150.00, type=TransactionType.DEBITO_SICOOB),
    Transaction(valor=200.00, type=TransactionType.CREDITO_AV_SICREDI),
    Transaction(valor=75.50, type=TransactionType.DINHEIRO),
]

DATA["26/12/2025"] = [
    Transaction(valor=100.00, type=TransactionType.PARCELADO_2_4_SICREDI),
    Transaction(valor=85.00, type=TransactionType.PIX_SICOOB),
    Transaction(valor=120.00, type=TransactionType.CREDIARIO),
]

DATA["27/12/2025"] = [
    Transaction(valor=300.00, type=TransactionType.RECEBIMENTO_CREDITARIO),
    Transaction(valor=45.00, type=TransactionType.DINHEIRO),
]


@dataclass
class AddRequest:
    day: str
    value: float
    type: TransactionType


def add(request: AddRequest):
    transaction = Transaction(valor=request.value, type=request.type)
    DATA[request.day].append(transaction)


def get_all() -> Dict[str, List[Transaction]]:
    return DATA
