from .Data import TransactionType

TRANSACTION_TYPE_LABELS = {
    TransactionType.DINHEIRO: "Dinheiro",
    TransactionType.PIX_SICREDI: "Pix Sicredi",
    TransactionType.PIX_SICOOB: "Pix Sicoob",
    TransactionType.DEBITO_SICREDI: "Débito Sicredi",
    TransactionType.DEBITO_SICOOB: "Débito Sicoob",
    TransactionType.CREDITO_AV_SICREDI: "Crédito Av Sicredi",
    TransactionType.CREDITO_AV_SICOOB: "Crédito Av Sicoob",
    TransactionType.PARCELADO_2_4_SICREDI: "Parcelado 2 a 4 Sicredi",
    TransactionType.PARCELADO_2_4_SICOOB: "Parcelado 2 a 4 Sicoob",
    TransactionType.PARCELADO_5_6_SICREDI: "Parcelado 5 a 6 Sicredi",
    TransactionType.PARCELADO_5_6_SICOOB: "Parcelado 5 a 6 Sicoob",
    TransactionType.CREDIARIO: "Crediário",
    TransactionType.RECEBIMENTO_CREDITARIO: "Recebimento Creditário",
    TransactionType.BONUS_CRED: "BonusCred",
}


def get_transaction_label(transaction_type: TransactionType) -> str:
    """Retorna o label em português para um tipo de transação."""
    return TRANSACTION_TYPE_LABELS.get(transaction_type, str(transaction_type))


def get_transaction_options() -> dict[str, TransactionType]:
    """Retorna um dicionário com labels em português mapeados para tipos de transação."""
    return {label: tipo for tipo, label in TRANSACTION_TYPE_LABELS.items()}
