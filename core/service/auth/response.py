from dataclasses import dataclass


@dataclass
class AuthTokensResponse:
    id: str
    username: str
    access_token: str
    refresh_token: str
