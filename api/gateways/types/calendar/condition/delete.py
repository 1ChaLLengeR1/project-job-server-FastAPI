from typing import TypedDict
from core.data.user import UserData


class ApplicationGatewayCalendarConditionDeleteResult(TypedDict, total=True):
    condition_id: str
    user_data: UserData