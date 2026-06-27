from fastapi import Request
from fastapi.responses import JSONResponse

from .exceptions import DebateException
from ..schemas import APIResponse

async def debate_exception_handler(request: Request, exc: DebateException):
    return JSONResponse(
        status_code=400,
        content=APIResponse(
            success=False,
            message=exc.message,
            data=None,
        ).model_dump(),
    )

async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": str(exc)
        },
    )