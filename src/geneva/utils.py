from typing import Any, Dict

from fastapi.responses import JSONResponse


def success(message: str, data: Dict[str, Any] | None = None) -> JSONResponse:
    payload = {"status": "success", "message": message}
    if data:
        payload["data"] = data
    return JSONResponse(content=payload)


def error(message: str, status_code: int = 400) -> JSONResponse:
    payload = {"status": "error", "message": message}
    return JSONResponse(content=payload, status_code=status_code)
