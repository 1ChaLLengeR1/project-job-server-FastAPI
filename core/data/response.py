from fastapi.responses import JSONResponse
from typing import TypedDict, Union, Dict, Any, List, Literal, Optional


class Error(TypedDict, total=True):
    message: str


class ErrorResponse(TypedDict, total=False):
    message: Optional[str]


class ResponseData(TypedDict, total=False):
    is_valid: bool
    data: Union[str, Dict[str, Any], List[Any], None]
    additional: Union[Dict[str, Any]] | None
    status_code: int
    status: Literal['ERROR', 'SUCCESS']


class ResponseApiData:
    def __init__(self, status: str, status_code: int, data=None, additional=None):
        self.status = status
        self.status_code = status_code
        self.data = data
        self.additional = additional

    def to_response(self) -> JSONResponse:
        return JSONResponse(
            content={
                'status': self.status,
                'status_code': self.status_code,
                'data': self.data,
                'additional': self.additional
            },
            status_code=self.status_code
        )


def create_success_response(id_valid: bool = True, status: Literal['ERROR', 'SUCCESS'] = "SUCCESS", data=None,
                            additional=None,
                            status_code: int = 200):
    return ResponseData(
        is_valid=id_valid,
        status=status,
        data=data,
        additional=additional,
        status_code=status_code
    )


def create_error_response(message: str, status_code: int, additional: Optional[dict] = None) -> ResponseData:
    return ResponseData(
        is_valid=False,
        status="ERROR",
        data=ErrorResponse(
            message=message,
        ),
        additional=additional,
        status_code=status_code
    )
