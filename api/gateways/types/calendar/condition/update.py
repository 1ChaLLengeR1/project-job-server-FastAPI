from typing import TypedDict


class ApplicationGatewayCalendarConditionUpdateResult(TypedDict, total=True):
    norm_hours: float
    hourly_rate: float
    condition_id: str
