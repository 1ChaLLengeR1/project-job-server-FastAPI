from typing import TypedDict

from core.data.user import UserData


class ApplicationGatewayTaskCreateResult(TypedDict, total=True):
    description: str
    time: int
    active: bool
    user_data: UserData
