from fastapi.responses import JSONResponse
from typing import TypedDict, Union, Dict, Any, List, Literal, Optional


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
