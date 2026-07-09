from typing import Any, Literal, TypedDict

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


class Error(TypedDict, total=True):
    message: str


class ErrorResponse(TypedDict, total=False):
    message: str | None


class ResponseData(TypedDict, total=False):
    is_valid: bool
    data: str | dict[str, Any] | list[Any] | None
    additional: dict[str, Any] | None
    status_code: int
    status: Literal["ERROR", "SUCCESS"]


class ResponseApiData:
    def __init__(self, status: str, status_code: int, data=None, additional=None):
        self.status = status
        self.status_code = status_code
        self.data = data
        self.additional = additional

    def to_response(self) -> JSONResponse:
        return JSONResponse(
            content=jsonable_encoder(
                {
                    "status": self.status,
                    "status_code": self.status_code,
                    "data": self.data,
                    "additional": self.additional,
                }
            ),
            status_code=self.status_code,
        )


def create_success_response(
    id_valid: bool = True,
    status: Literal["ERROR", "SUCCESS"] = "SUCCESS",
    data=None,
    additional=None,
    status_code: int = 200,
):
    return ResponseData(is_valid=id_valid, status=status, data=data, additional=additional, status_code=status_code)


def create_error_response(message: str, status_code: int, additional: dict | None = None) -> ResponseData:
    return ResponseData(
        is_valid=False,
        status="ERROR",
        data=ErrorResponse(
            message=message,
        ),
        additional=additional,
        status_code=status_code,
    )
