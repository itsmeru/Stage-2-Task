from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    error_messages = []
    for error in errors:
        print(error)
        field = error["loc"][-1]
        message = error["msg"]
        error_messages.append(f"{field}: {message}")
    data = {"error": True, "message": error_messages}
    return JSONResponse(status_code=422, content=data)

async def custom_http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401:
        return JSONResponse(status_code=403, content={"error": True, "message": "未登入系統，拒絕存取"})
    elif exc.status_code == 400:
        return JSONResponse(status_code=400, content={"error": True, "message": "建立失敗，輸入不正確或其他原因"})
    else:
        return JSONResponse(status_code=exc.status_code, content={"error": True, "message": exc.detail})
