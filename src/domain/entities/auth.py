from dataclasses import dataclass
from typing import Optional, List


@dataclass
class AuthResponse:
    token: str
    refresh_token: str
    user: dict

    @staticmethod
    def from_dict(data: dict) -> "AuthResponse":
        return AuthResponse(
            token=data["token"],
            refresh_token=data["refresh_token"],
            user=data["user"],
        )


@dataclass
class LoginRequest:
    email: str
    password: str

    def to_dict(self) -> dict:
        return {
            "email": self.email,
            "password": self.password,
        }


@dataclass
class RegisterRequest:
    email: str
    password: str
    name: str
    company_name: str
    cnpj: str

    def to_dict(self) -> dict:
        return {
            "email": self.email,
            "password": self.password,
            "name": self.name,
            "company_name": self.company_name,
            "cnpj": self.cnpj,
        }
