from typing import TypedDict


class UserData(TypedDict, total=False):
    id: str
    username: str
