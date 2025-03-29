from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from typing import Any, Optional


def response_success(
    data: Optional[Any] = None, message: str = "Success", status_code: int = 200
) -> JSONResponse:
    return JSONResponse(
        content={
            "code":status_code,
            "message": message,
            "data": data,
        },
        status_code=status_code,
    )