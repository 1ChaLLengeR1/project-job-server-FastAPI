from typing import TypedDict, Union, Dict, Any, List, Literal, Optional
from core.data.user import UserData


class ApplicationGatewayTaskCreateResult(TypedDict, total=True):
    description: str
    time: int
    active: bool
    user_data: UserData
