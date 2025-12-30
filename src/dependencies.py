from infrastructure.http import HTTPClient
from infrastructure.api import (
    PaymentModalityAPIRepository,
    FinancialEntryAPIRepository,
)
from infrastructure.api.auth_api_repository import AuthAPIRepository
from infrastructure.api.company_api_repository import CompanyAPIRepository
from infrastructure.api.user_api_repository import UserAPIRepository
from application.use_cases import PaymentModalityUseCases, FinancialEntryUseCases
from application.use_cases.auth_use_cases import AuthUseCases
from application.use_cases.admin_use_cases import AdminUseCases


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

            # Existing repositories
            self._payment_modality_repository = PaymentModalityAPIRepository(
                self._http_client
            )
            self._financial_entry_repository = FinancialEntryAPIRepository(
                self._http_client
            )

            # New repositories
            self._auth_repository = AuthAPIRepository(self._http_client)
            self._company_repository = CompanyAPIRepository(self._http_client)
            self._user_repository = UserAPIRepository(self._http_client)

            # Existing use cases
            self._payment_modality_use_cases = PaymentModalityUseCases(
                self._payment_modality_repository
            )
            self._financial_entry_use_cases = FinancialEntryUseCases(
                self._financial_entry_repository
            )

            # New use cases
            self._auth_use_cases = AuthUseCases(self._auth_repository)
            self._admin_use_cases = AdminUseCases(
                self._company_repository,
                self._user_repository
            )

            Container._initialized = True

    @property
    def http_client(self) -> HTTPClient:
        return self._http_client

    @property
    def payment_modality_use_cases(self) -> PaymentModalityUseCases:
        return self._payment_modality_use_cases

    @property
    def financial_entry_use_cases(self) -> FinancialEntryUseCases:
        return self._financial_entry_use_cases

    @property
    def auth_use_cases(self) -> AuthUseCases:
        return self._auth_use_cases

    @property
    def admin_use_cases(self) -> AdminUseCases:
        return self._admin_use_cases


def get_container() -> Container:
    return Container()
