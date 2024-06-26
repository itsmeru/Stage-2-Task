from fastapi import FastAPI, HTTPException,Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from controller import attractionId, attractions, buildSchedule, getUser, mrts, signIn, signUp, getSchedule,deleteSchedule
from database import create_db_pool
from starlette_session import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware

from view import staticPages

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.add_middleware(
#     SessionMiddleware,
#     secret_key="ruruisthebest",
#     max_age=3600,
#     cookie_name="session_data",    
# )


db_pool ={
    "spot":create_db_pool("spot"),
}
@app.middleware("http")
async def attach_db_connection(request, call_next):
    request.state.db_pool = db_pool
    response = await call_next(request)
    return response

@app.exception_handler(RequestValidationError)
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

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401:
        return JSONResponse(status_code=403,content={"error":True,"message":"未登入系統，拒絕存取"})
    elif exc.status_code == 400:
        return JSONResponse(status_code=400,content={"error":True,"message":"建立失敗，輸入不正確或其他原因"},)

app.include_router(attractions.router)
app.include_router(mrts.router)
app.include_router(staticPages.router)
app.include_router(attractionId.router)
app.include_router(signUp.router)
app.include_router(signIn.router)
app.include_router(getUser.router)
app.include_router(buildSchedule.router)
app.include_router(getSchedule.router)
app.include_router(deleteSchedule.router)





