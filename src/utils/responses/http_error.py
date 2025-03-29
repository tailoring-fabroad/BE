from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse


async def response_error(_: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse({"errors": [exc.detail]}, status_code=exc.status_code)
