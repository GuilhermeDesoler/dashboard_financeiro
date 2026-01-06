from infrastructure.http import HTTPClient
from infrastructure.api import (
    PaymentModalityAPIRepository,
    FinancialEntryAPIRepository,
)
from infrastructure.api.auth_api_repository import AuthAPIRepository
from infrastructure.api.company_api_repository import CompanyAPIRepository
from infrastructure.api.user_api_repository import UserAPIRepository
from infrastructure.api.platform_settings_api_repository import PlatformSettingsAPIRepository
from infrastructure.api.installment_api_repository import InstallmentAPIRepository
from infrastructure.api.account_api_repository import AccountAPIRepository
from infrastructure.api.bank_limit_api_repository import BankLimitAPIRepository
from application.use_cases import PaymentModalityUseCases, FinancialEntryUseCases
from application.use_cases.auth_use_cases import AuthUseCases
from application.use_cases.admin_use_cases import AdminUseCases
from application.use_cases.platform_settings_use_cases import PlatformSettingsUseCases
from application.use_cases.installment_use_cases import InstallmentUseCases
from application.use_cases.account_use_cases import AccountUseCases
from application.use_cases.bank_limit_use_cases import BankLimitUseCases


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
            self._company_repository = CompanyAPIRepository(self._http_client)
            self._user_repository = UserAPIRepository(self._http_client)
            self._platform_settings_repository = PlatformSettingsAPIRepository(self._http_client)
            self._installment_repository = InstallmentAPIRepository(self._http_client)
            self._account_repository = AccountAPIRepository(self._http_client)
            self._bank_limit_repository = BankLimitAPIRepository(self._http_client)

            self._payment_modality_use_cases = PaymentModalityUseCases(
                self._payment_modality_repository
            )
            self._financial_entry_use_cases = FinancialEntryUseCases(
                self._financial_entry_repository
            )

            self._auth_use_cases = AuthUseCases(self._auth_repository)
            self._admin_use_cases = AdminUseCases(
                self._company_repository,
                self._user_repository
            )
            self._platform_settings_use_cases = PlatformSettingsUseCases(
                self._platform_settings_repository
            )
            self._installment_use_cases = InstallmentUseCases(
                self._installment_repository
            )
            self._account_use_cases = AccountUseCases(
                self._account_repository
            )
            self._bank_limit_use_cases = BankLimitUseCases(
                self._bank_limit_repository
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

    @property
    def platform_settings_use_cases(self) -> PlatformSettingsUseCases:
        return self._platform_settings_use_cases

    @property
    def installment_use_cases(self) -> InstallmentUseCases:
        return self._installment_use_cases

    @property
    def account_use_cases(self) -> AccountUseCases:
        return self._account_use_cases

    @property
    def bank_limit_use_cases(self) -> BankLimitUseCases:
        return self._bank_limit_use_cases


def get_container() -> Container:
    return Container()
