from typing import TypedDict
from core.data.user import UserData


class ApplicationGatewayCalendarConditionCreateResult(TypedDict, total=True):
    norm_hours: float
    hourly_rate: float
    user_data: UserData