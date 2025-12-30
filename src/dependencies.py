from infrastructure.http import HTTPClient
from infrastructure.api import (
    PaymentModalityAPIRepository,
    FinancialEntryAPIRepository,
    AuthAPIRepository,
)
from application.use_cases import (
    PaymentModalityUseCases,
    FinancialEntryUseCases,
    AuthUseCases,
)


class Container:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not Container._initialized:
            self._http_client = HTTPClient()

            self._payment_modality_repository = PaymentModalityAPIRepository(
                self._http_client
            )
            self._financial_entry_repository = FinancialEntryAPIRepository(
                self._http_client
            )
            self._auth_repository = AuthAPIRepository(self._http_client)

            self._payment_modality_use_cases = PaymentModalityUseCases(
                self._payment_modality_repository
            )
            self._financial_entry_use_cases = FinancialEntryUseCases(
                self._financial_entry_repository
            )
            self._auth_use_cases = AuthUseCases(self._auth_repository)

            Container._initialized = True

    @property
    def payment_modality_use_cases(self) -> PaymentModalityUseCases:
        return self._payment_modality_use_cases

    @property
    def financial_entry_use_cases(self) -> FinancialEntryUseCases:
        return self._financial_entry_use_cases

    @property
    def auth_use_cases(self) -> AuthUseCases:
        return self._auth_use_cases


def get_container() -> Container:
    return Container()
